import express from "espress";
const app = express();
const port = 3000;

app.use(express.json());

app.get("/", (_, res) => {
    res.send("1");
});

app.listen(port, () => {
    console.log(`http://localhost:${port}`);
});