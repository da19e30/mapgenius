const mongoose = require('mongoose');
require('dotenv').config();

const connectDB = async () => {
  try {
    const conn = await mongoose.connect(process.env.DATABASE_URL || 'mongodb://localhost:27017/mapgenius_db', {
      useNewUrlParser: true,
      useUnifiedTopology: true,
      serverApi: {
        version: "1",
        strict: true,
        deprecationErrors: true,
      }
    });

    console.log(`MongoDB conectado: ${conn.connection.host}`);
    return conn;
  } catch (error) {
    console.error('Error al conectar a MongoDB:', error.message);
    process.exit(1);
  }
};

module.exports = connectDB;