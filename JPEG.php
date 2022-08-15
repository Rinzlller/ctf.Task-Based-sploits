<?php

function only_jpeg() {
    danger("Only JPEG images are allowed!");
}

if (!isset($_FILES["file"])) {
    return;
}

if ($_FILES["file"]["type"] !== "image/jpeg") {
    only_jpeg();
    return;
}

$name = $_FILES["file"]["name"];

$tmp_name = $_FILES["file"]["tmp_name"];
$img = imagecreatefromjpeg($tmp_name);

if (!$img) {
    only_jpeg();
    return;
}

list($width, $height) = getimagesize($tmp_name);

if ($width > 1000 || $height > 1000) {
    danger("Too big!");
    return;
}

$newheight = 168;
$newwidth = $width / $height * $newheight;

$thumb = imagecreatetruecolor($newwidth, $newheight);
if (!imagecopyresized($thumb, $img, 0, 0, 0, 0,
    $newwidth, $newheight, $width, $height)) {
    danger("Failed to resize");
    return;
}

if (!imagejpeg($img, $tmp_name, 90)) {
    danger("Failed to save");
    return;
}

$dir = "uploads/" . uniqid();
mkdir($dir);
$file = $dir . "/" . $name;

if (!move_uploaded_file($tmp_name, $file)) {
    error();
    return;
}

success("Image uploaded and resized successfully!");

?>