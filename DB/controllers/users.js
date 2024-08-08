import {client} from "../db.js";

const getUsers = async (_, res) => {

    const rows = await client.query('SELECT * FROM alumnos');
    res.json(rows);
    }

const getUser = async (req, res) => {

    const id = req.params.id
    const rows = await conn.query("SELECT * FROM artistas WHERE id = $1", [id])
    res.json(rows[0])
}

const createUser = async (req, res) => {

    const user = req.body
    const email = req.body
    const contraseña = req.body
    await conn.query("INSERT INTO usuarios (user, email, contraseña ) VALUES ($1)", [user], [email], [contraseña])
    res.json(user)
};

const users = {
    getUsers,
    getUser,
    createUser
};

export default users;