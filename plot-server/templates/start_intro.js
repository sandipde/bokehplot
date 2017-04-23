function startIntro(){
  var intro = introJs();
    intro.setOptions({
      steps: [
        { 
          intro: "<h3 class='w3-center w3-blue-grey' style='width:300px; text-align:justify '> What is Sketchmap ? </h3> <br> <p style='text-align:justify; width:300px;'>Sketch-map is a non-linear dimensionality reduction algorithm that is particularly well suited to examining the high-dimensionality data that is routinely produced in atomistic simulations. It transforms the connectivity between a set of high dimensionality data points in 2-dimension while putting higher importance to proximity matching. While the similarity between a pair of atomic structures can be measured in various ways, we used SOAP-REMatch kernel, developed in our group for this purpose.</p>"
        },
        {
          element: document.querySelector('#step1'),
          intro: "<p style='width:300px; text-align:justify'>This is your interactive sketchmap panel. You can pan, zoom  or select the points. Each point on the plot represents an atomic configuration. If two structures are similar the points are close in the map. Clustering of points signifies a common structural motif. </p>",
        position: 'right'
        },
        
        {
          element: document.querySelectorAll('#step2')[0],
          intro: "<p style='width:300px; text-align:justify'> You can visualize the atomic structure here by selecting a point on the map with your mouse </p>",
          position: 'bottom'
        },
        {
          element: document.querySelectorAll('#step3')[0],
          intro: "<p style='width:300px; text-align:justify'>This second atomic structure visualizer is bound to the slider at the bottom of the plot. The selected configuration also shows up on the map as blue point. This provides a second way of selecting a structure and compare it with the first one. </p>",
          position: 'top'
        },
        {
          element: '#step4',
          intro: "<p style='width:300px; text-align:justify'>That's all you need to know for now. Have fun with Sketchmap !  </p>"
        },
      ]
    });
    intro.start();
}
