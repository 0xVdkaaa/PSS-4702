<?php
$servername = "mysql-db"; // GUNAKAN nama service dari docker-compose.yml
$username = "user";
$password = "password";
$dbname = "testdb";

$conn = mysqli_connect($servername, $username, $password, $dbname);

if (!$conn) {
    die("Failed to connect to MySQL: " . mysqli_connect_error());
}
echo "✅ Connected successfully to MySQL in Docker!";
?>
