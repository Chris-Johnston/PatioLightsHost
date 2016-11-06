<!DOCTYPE HTML>
<html lang="en" xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta charset="utf-8" />
    <title>Patio Lights Color Picker</title>
    <link rel="stylesheet" type="text/css" href="css/style.css" />
    <!-- uses jscolor for color picker jscolor.com -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jscolor/2.0.4/jscolor.js"></script>
    <!-- Google Web Fonts -->
    <link href='https://fonts.googleapis.com/css?family=Oswald|Roboto+Condensed:400,400italic,700italic,700,300' rel='stylesheet' type='text/css'>
</head>
<body>
    <div id="header">
        <h1>Patio Lights Color Picker</h1>
        <a id="githublink" href="https://github.com/chris-johnston">github.com/Chris-Johnston</a>
    </div>
    <div id="wrapper">
        <div id="inner">
            <div id="status">
                Your information has been entered.
                <br />
                <!-- wrap the php output in code. it'll just output json -->
                <div id="phpOutput">
                <?php 
                // open the colorData file so we can write to it
                $fileName = "colorData.json";
                $colorDataFile = fopen("colorData.json", "w+") or die("File error");
                // get each of the parameters from the form
                $color1 = $_GET["color1"];
                $color2 = $_GET["color2"];
                $bulb1 = $_GET["bulb1"];
                $bulb2 = $_GET["bulb2"];
                $bulb3 = $_GET["bulb3"];
                $stripPattern = $_GET["stripPattern"];
                $bulbPattern = $_GET["bulbPattern"];
                $stripDelay1 = $_GET["stripDelay1"];
                $bulbDelay1 = $_GET["bulbDelay1"];

                function hexToRGB($hexColorValue)
                {
                    // remove any # from the hex value
                    $hex = str_replace("#", "", $hexColorValue);
                    if(strlen($hex) == 3) {
                        $_r = hexdec(substr($hex,0,1).substr($hex,0,1));
                        $_g = hexdec(substr($hex,1,1).substr($hex,1,1));
                        $_b = hexdec(substr($hex,2,1).substr($hex,2,1));
                    } else {
                        $_r = hexdec(substr($hex,0,2));
                        $_g = hexdec(substr($hex,2,2));
                        $_b = hexdec(substr($hex,4,2));
                    }
                    $rgb = array($_r, $_g, $_b);
                    //return implode(",", $rgb); // returns the rgb values separated by commas
                    return $rgb; // returns an array with the rgb values
                }

                $stripColor1 = hexToRGB($color1);
                $stripColor2 = hexToRGB($color2);
                $bulbColor1 = hexToRGB($bulb1);
                $bulbColor2 = hexToRGB($bulb2);
                $bulbColor3 = hexToRGB($bulb3);

                // testing stuff
                /*echo $stripColor1;
                echo $stripColor2;
                echo $bulbColor1;
                echo $bulbColor2;
                echo $bulbColor3;*/

                // save to an array

                // use this one if I want an array of r,g,b instead of hex values
                
                $data = array (
                    "stripColor1" => $stripColor1,
                    "stripColor2" => $stripColor2, 
                    "bulbColor1" => $bulbColor1,
                    "bulbColor2" => $bulbColor2,
                    "bulbColor3" => $bulbColor3,
                    "stripPattern" => $stripPattern,
                    "bulbPattern" => $bulbPattern,
                    "stripDelay1" => $stripDelay1,
                    "bulbDelay1" => $bulbDelay1
                    );
                
                /*
                $data = array (
                    "stripColor1" => $color1,
                    "stripColor2" => $color2, 
                    "bulbColor1" => $bulb1,
                    "bulbColor2" => $bulb2,
                    "bulbColor3" => $bulb3,
                    "stripPattern" => $stripPattern,
                    "bulbPattern" => $bulbPattern,
                    "stripDelay1" => $stripDelay1,
                    "bulbDelay1" => $bulbDelay1
                    ); */
                // write to json file
                $jsonData = json_encode($data);
                echo $jsonData;
                file_put_contents($fileName, $jsonData);
                fclose($colorDataFile);
                ?>
                </div>
            </div>
            <br />
            <a href="index.html">Return the the color picker.</a>
        </div>
    </div>
</body>
</html>
