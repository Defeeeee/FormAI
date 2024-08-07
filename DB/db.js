import { Client } from "pg";
import dotenv from 'dotenv';

dotenv.config();

export const client = new Client({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASS,
    database: process.env.DB_NAME,
    port: 3000,
});

client.connect(); 
