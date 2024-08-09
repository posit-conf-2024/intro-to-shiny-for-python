
// Listens to message from iframe
document.addEventListener('DOMContentLoaded', function() {
  window.addEventListener('message', handleYourturnMessage, false)
    function handleYourturnMessage(event) {
    console.log("Message from yourturn iframe:", event.data) // outputs: {foo: 'bar'}
    if (typeof event.data === 'string' && event.data.trim() !== '') {
        document.getElementById('messageDisplay').innerText = event.data;
        // Create a new iframe element
        var newIframe = document.createElement('iframe');
        newIframe.src = event.data; // Use the message as the src
        newIframe.height = "1200px";
        newIframe.width = "100%";
        newIframe.style.border = "1px solid #123233";
        newIframe.id = "yourturnIframe";
        
        // Insert the new iframe into the DOM
        var iframeContainer = document.getElementById('yourturnContainer');
        iframeContainer.innerHTML = ''; // Clear any previous iframes
        iframeContainer.appendChild(newIframe);
        
        // Inject CSS to hide elements in the iframe
        newIframe.onload = function() {
            var iframeDocument = newIframe.contentDocument || newIframe.contentWindow.document;
            var style = iframeDocument.createElement('style');
            style.innerHTML = `
            #quarto-header { display: none !important; }
            #quarto-sidebarnav-toggle { display: none !important; }
            `;
            iframeDocument.head.appendChild(style);
        };
        
        // change Z index of quarto sidebar
        document.getElementById("yourturnContainer").style.zIndex = 1
    }
    // Resize the iframe
    iframeResize({
      license: 'GPLv3',
      waitForLoad: true,
    }, '#yourturnIframe');
  }
});


