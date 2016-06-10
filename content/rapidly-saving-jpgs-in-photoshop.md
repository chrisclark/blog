Title: Rapidly Saving .jpgs in Photoshop
Date: 2012-10-17 23:52
Author: Chris Clark()
Slug: rapidly-saving-jpgs-in-photoshop

**Cliffs notes**: Now, whenever I hit F2 in Photoshop, I get a high
quality jpg of my file saved to the same directory. No more
"File-&gt;Save As" nonsense every time I want a static version of the
image.  
  
**What/how/why:** I was working on some product mock-ups this morning in
Photoshop using layers to show and hide different bits of the mockup,
depending on the state of the application. It was time to wire all of
the various states together in a clickable mock-up (I use
[invisionapp.com](http://invisionapp.com/) to do this - highly
recommended) so I needed to save off a whole bunch of images from
Photoshop, with different layers set to visible. I quickly tired of
going to File-&gt;Save As-&gt;Select Jpg file type-&gt;\[Type file
name\]-&gt;Hit save. There has to be a better way!  
  
After Googling some options (I am not a PS expert), I decided to create
a script that would save the image as a jpg, with a unique name
generated from a timestamp. I found some sample code for the various
pieces and came up with the script below:  

    :::javascript
    //Cobbled together from:
    //http://feedback.photoshop.com/photoshop_family/topics/quick_save_as
    //http://www.polycount.com/forum/showthread.php?t=85425
    
    #target photoshop;
    
    if (app.documents.length > 0) {
      var thedoc = app.activeDocument;
      
      var docName = thedoc.name;
      if (docName.indexOf(".") != -1) {
        var basename = docName.match(/(.*)\.[\^\.]+\$/)[1]
      } else {
        var basename = docName
      }
      
      //getting the location, if unsaved save to desktop;
      try {
        var docPath = thedoc.path
      } catch (e) {
        var docPath = "\~/Desktop"
      }
      
      var jpegOptions = new JPEGSaveOptions();
      jpegOptions.quality = 9;
      jpegOptions.embedColorProfile = true;
      jpegOptions.matte = MatteType.NONE;
      
      var filename = docPath + '/' + basename + "-" + getTime() + '.jpg';
      
      thedoc.saveAs((new File(filename)), jpegOptions, true);
    }; 
      
    function getTime(){
      var currentTime = new Date();
      
      //Make single-digit mins show up as 6:01 and not 6:1
      var minutes = currentTime.getMinutes();
      if (minutes < 10) {
        minutes = "0" + minutes;
      }
      
      var timeStamp = currentTime.getFullYear() + "-"
      + (currentTime.getMonth() + 1) + "-"
      + currentTime.getDate() + "-"
      + currentTime.getHours() + "."
      + minutes + "."
      + currentTime.getSeconds() + "."
      + currentTime.getMilliseconds();
      return timeStamp;
    }

If you save this as "Quick
save to jpg.jsx" to \\Program Files\\Adobe\\Adobe Photoshop
CS5.1\\Presets\\Scripts, you will then be able to access the script by
going to File-&gt;Scripts. I went one step further and recorded an
action of the script firing and bound it to my f2 key.
  
Now, whenever I'm in Photoshop, I can just hit f2 and get a .jpg image
saved to my current directory, with no dialogs or anything! Neat!
