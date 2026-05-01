/// <reference types="cypress" />

describe('Invoice Wizard End-to-End', () => {
  it('creates a new invoice successfully', () => {
    // Assume user is already logged in via a programmatic token set in localStorage
    cy.visit('/invoice-wizard');

    // Wait for clients and products to load
    cy.contains('Cliente').should('exist');
    cy.get('select').first().select(1); // select first client option

    // Add a line item
    cy.contains('Añadir línea').click();
    // Select product (first option)
    cy.get('select').eq(1).select(1);
    // Set quantity
    cy.get('input[type="number"]').eq(0).clear().type('2');

    // Submit the form
    cy.contains('Crear Factura').click();

    // Verify success message includes CUFE and status
    cy.contains('Factura creada con CUFE').should('be.visible');
  });
});
