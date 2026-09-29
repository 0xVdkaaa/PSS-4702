const express = require('express');
const app = express();
const port = 3000;

app.get('/', (req, res) => {
  res.send('Hello from Express JS in Docker!');
});

app.listen(port, () => {
  console.log(`App running on port ${port}`);
});