Jmol._isAsync = false;
var jmolApplet0; // set up in HTML table, below
jmol_isReady = function(applet) {
document.title = (applet._id + " - Jmol " + Jmol.___JmolVersion)
Jmol._getElement(applet, "appletdiv").style.border="0px solid blue"
}

var Info = {
width: 400,
height: 400,
debug: false,
color: "0xFFFFFF",
use: "HTML5",   // JAVA HTML5 WEBGL are all options
j2sPath: "static/jmol/j2s", // this needs to point to where the j2s directory is.
jarPath: "static/jmol/java",// this needs to point to where the java directory is.
jarFile: "JmolAppletSigned.jar",
isSigned: true,
script: "set antialiasDisplay;load plot-server/static/set.0001.xyz; connect 1.0 1.2 (carbon) (hydrogen) SINGLE CREATE ; connect 1.0 1.2 (nitrogen) (hydrogen) SINGLE CREATE ; connect 1.0 4.2 (carbon) (nitrogen) SINGLE CREATE ; connect 3.0 6 (phosphorus) (iodine) SINGLE CREATE ; set perspectiveDepth OFF " ,
serverURL: "./jmol/php/jsmol.php",
readyFunction: jmol_isReady,
disableJ2SLoadMonitor: true,
disableInitialConsole: true,
allowJavaScript: true
}

$(document).ready(function() {
$("#appdiv").html(Jmol.getAppletHtml("jmolApplet0", Info))
})
var lastPrompt=0;