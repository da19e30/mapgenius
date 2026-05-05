# Mapgenius Solutions - Backend Core Architecture (NestJS)

This document outlines the foundational code structure for the electronic invoicing SaaS, implementing the UBL 2.1 standard and DIAN integration.

## 1. Project Structure (Modular)
```text
src/
├── modules/
│   ├── auth/              # JWT & Multi-tenant security
│   ├── companies/         # Resolution & Certificate management
│   ├── invoicing/         # Core UBL 2.1 Logic
│   │   ├── services/
│   │   │   ├── ubl-generator.service.ts
│   │   │   ├── cufe-calculator.service.ts
│   │   │   ├── xades-signer.service.ts
│   │   │   └── dian-integration.service.ts
│   │   ├── invoicing.controller.ts
│   │   └── invoicing.module.ts
│   ├── ai/                # OpenAI/Anthropic OCR & Analysis
│   └── clients/           # Fiscal data management
└── shared/
    ├── decorators/        # TenantID decorators
    └── interfaces/        # UBL 2.1 JSON Schemas
```

## 2. Core Service: UBL 2.1 Generator (Preview)
This service transforms business data into the XML format required by the DIAN.

```typescript
// invoicing/services/ubl-generator.service.ts
import { Injectable } from '@nestjs/common';
import * as xmlbuilder from 'xmlbuilder';

@Injectable()
export class UblGeneratorService {
  generateInvoiceXml(data: any): string {
    const xml = xmlbuilder.create('Invoice', { encoding: 'UTF-8' })
      .att('xmlns', 'urn:oasis:names:specification:ubl:schema:xsd:Invoice-2')
      .att('xmlns:cac', 'urn:oasis:names:specification:ubl:schema:xsd:CommonAggregateComponents-2')
      .att('xmlns:cbc', 'urn:oasis:names:specification:ubl:schema:xsd:CommonBasicComponents-2')
      // ... Add additional namespaces (ext, ds, sts)
      
    xml.ele('cbc:UBLVersionID', 'UBL 2.1');
    xml.ele('cbc:CustomizationID', '1');
    xml.ele('cbc:ProfileID', 'DIAN 2.1');
    xml.ele('cbc:ID', data.number);
    xml.ele('cbc:UUID', { 'schemeID': '2', 'schemeName': 'CUFE' }, data.cufe);
    xml.ele('cbc:IssueDate', data.date);
    
    // Accounting Supplier Party (Emisor)
    const supplier = xml.ele('cac:AccountingSupplierParty').ele('cac:Party');
    // ... logic to map issuer NIT, Address, Tax Scheme
    
    return xml.end({ pretty: true });
  }
}
```

## 3. Core Service: CUFE Calculator (SHA-384)
The CUFE is mandatory for every electronic invoice in Colombia.

```typescript
// invoicing/services/cufe-calculator.service.ts
import * as crypto from 'crypto';

export class CufeCalculatorService {
  calculate(data: InvoiceData, softwarePin: string): string {
    // Standard concatenation order by DIAN
    const rawString = 
      data.number + 
      data.issueDate + 
      data.issueTime + 
      data.valImp + 
      data.codImp1 + 
      data.valImp1 + 
      // ... other fields
      softwarePin;

    return crypto.createHash('sha384').update(rawString).digest('hex');
  }
}
```

## 4. DIAN SOAP Integration (Asynchronous)
Handling the communication with the DIAN Web Services.

```typescript
// invoicing/services/dian-integration.service.ts
import { Injectable } from '@nestjs/common';
import { InjectQueue } from '@nestjs/bull';
import { Queue } from 'bull';

@Injectable()
export class DianIntegrationService {
  constructor(@InjectQueue('dian-submissions') private dianQueue: Queue) {}

  async submitInvoice(signedXml: string, tenantId: string) {
    // Add to Redis queue for background processing
    await this.dianQueue.add('send-to-dian', {
      xml: signedXml,
      tenantId,
      retries: 3
    });
  }
}
```

## 5. Security: Multi-tenant Isolation
Ensuring data privacy across different companies.

```typescript
// shared/interceptors/tenant.interceptor.ts
@Injectable()
export class TenantInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const tenantId = request.user.tenantId; // From JWT
    // Inject tenantId into all DB queries
    return next.handle();
  }
}
```