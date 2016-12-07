function setPreset(buttonSrc)
{
    // gets the id of the button that fired the onclick event
    var sourceID = buttonSrc.id;

    // get the form where all of the data is
    var form = document.forms[0];

    switch(sourceID)
    {
	case "presetOff":
            // preset that turns everything off
	    form["bulb1"].value = "000000";
	    form["bulb2"].value = "000000";
            form["bulb3"].value = "000000";
            form["color1"].value = "000000";
            form["color2"].value = "000000";
            form["stripPattern"].value = "0";
        case "presetRedWhiteBlue":
            // preset for red white and blue lights
            form["bulb1"].value = "FF0000";
            form["bulb2"].value = "FFFFFF";
            form["bulb3"].value = "0000FF";
            form["stripPattern"].value = "a";
            form["bulbPattern"].value = "1";
            form["stripDelay1"].value = 5000;
            form["width"].value = 50;
            break;
        case "presetGameDay":
            // preset for seahawks game day
            // blue and green smooth scroll
            // with green and blue lights
            form["color1"].value = "00FF00";
            form["color2"].value = "0000FF";
            form["stripPattern"].value = "4";
            form["stripDelay1"].value = 4000;
            form["width"].value = 30;
            form["bulb1"].value = "00FF00";
            form["bulb2"].value = "000000";
            form["bulb3"].value = "0000FF";
            form["bulbPattern"].value = "1";
            break;
        case "presetXMAS":
            // preset for xmas lights
            // green and red
            form["color1"].value = "00FF00";
            form["color2"].value = "FF0000";
            form["stripPattern"].value = "3";
            form["stripDelay1"].value = 100;
            form["width"].value = 10;
            form["bulb1"].value = "FFFFFF";
            form["bulbPattern"].value = "0";
            break;

        default:
        case "presetNormal":
            // normal looking lights
            // aka boring. all white color
            form["color1"].value = "FFFFFF";
            form["stripPattern"].value = "0";
            form["bulb1"].value = "FFFFFF";
            form["bulbPattern"].value = "0";
            break;
    }
    // todo more presets?
    // todo need to find a way to update the background of jscolor pickers
    // they don't update when I change the values in this
}
