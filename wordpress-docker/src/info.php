<?php
$servername = "mysql"; // gunakan nama service dari docker-compose.yml
$username = "a71b";
$password = "a71b";
$dbname = "wordpress_dp";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
  die("Connection failed: " . $conn->connect_error);
}

echo "✅ Connected successfully to MySQL!<br>";

$redis = new Redis();
$redis->connect('redis', 6379);
echo "✅ Connected successfully to Redis!";
?>
