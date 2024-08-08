import {client} from "../db.js";

const getUsers = async (_, res) => {
    const [rows] = await client.query('SELECT * FROM alumnos');
    res.json(rows);
    }

const users = {
    getUsers,
};

export default users;