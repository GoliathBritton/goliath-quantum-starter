import axios from 'axios';
import mysql from 'mysql2/promise';

const GHL_API = `https://rest.gohighlevel.com/v1`;
const GHL_API_KEY = process.env.GHL_API_KEY;
const DB_CONFIG = {
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
};

export default async function handler(req, res) {
    if (req.method === 'POST') {
        const event = req.body;
        console.log('Received GHL Event:', event);

        try {
            const db = await mysql.createConnection(DB_CONFIG);
            const { id, first_name, last_name, email, phone } = event.contact || {};

            if (id && first_name && last_name && email && phone) {
                await db.execute(
                    'INSERT INTO leads (id, first_name, last_name, email, phone, created_at) VALUES (?, ?, ?, ?, ?, ?)',
                    [id, first_name, last_name, email, phone, new Date()]
                );
                console.log('Lead saved to database:', { id, first_name, last_name, email, phone });
                res.status(200).send('Lead received and saved');
            } else {
                console.warn('Received GHL event without complete lead data:', event);
                res.status(400).send('Incomplete lead data received');
            }
            db.end();
        } catch (error) {
            console.error('Error processing webhook:', error);
            res.status(500).send('Internal Server Error');
        }
    } else {
        res.setHeader('Allow', ['POST']);
        res.status(405).end(`Method ${req.method} Not Allowed`);
    }
}