Jmol._isAsync = false;
var jmolApplet1; // set up in HTML table, below
jmol_isReady = function(applet) {
document.title = (applet._id + " - Jmol " + Jmol.___JmolVersion)
Jmol._getElement(applet, "appletdiv").style.border="0px solid blue"
}

var Info = {
width: 300,
height: 300,
debug: false,
color: "0xFFFFFF",
use: "HTML5",   // JAVA HTML5 WEBGL are all options
j2sPath: "{{dir}}/static/jmol/j2s", // this needs to point to where the j2s directory is.
jarPath: "{{dir}}/static/jmol/java",// this needs to point to where the java directory is.
jarFile: "JmolAppletSigned.jar",
isSigned: true,
script: "set antialiasDisplay; load {{dir}}/static/xyz/set.0000.xyz; connect 1.0 1.2 (carbon) (hydrogen) SINGLE CREATE ; connect 1.0 1.2 (nitrogen) (hydrogen) SINGLE CREATE ; connect 1.0 1.2 (carbon) (nitrogen) SINGLE CREATE ; connect 3.0 6 (phosphorus) (iodine) SINGLE CREATE ; set perspectiveDepth OFF ; Spin on" ,
serverURL: "./jmol/php/jsmol.php",
readyFunction: jmol_isReady,
disableJ2SLoadMonitor: true,
disableInitialConsole: true,
allowJavaScript: true
}

$(document).ready(function() {
$("#appdiv2").html(Jmol.getAppletHtml("jmolApplet1", Info))
})
var lastPrompt=0;
