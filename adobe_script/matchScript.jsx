
app.project.createNewSequence("test","C:\\Program Files\\Adobe\\Adobe Premiere Pro CC 2017\\Settings\\SequencePresets\\ARRI\\1080p\\ARRI 1080p 30fps.sqpreset", 0)

var meta_file = File.openDialog("Selection prompt");
var meta_string = meta_file.toString();
var file_length = meta_string.lastIndexOf("/") + 1;
var file_path = meta_string.substr(0,file_length)

if(meta_file !== false){// if it is really there
          meta_file.open('r'); // open it
          meta_content = meta_file.read(); // read it
          meta_data =  JSON.parse(meta_content);// now evaluate the string from the file
          //alert(events.toSource()); // if it all went fine we have now a JSON Object instead of a string call length
          meta_file.close(); // always close files after reading
          }else{
          alert("Bah!"); // if something went wrong
}

var count = 1
for (i = 0; i < meta_data["infographics"].length; i++){
    var game_number = meta_data["infographics"][i].substr(1,1)
    var game = parseInt(game_number);
    if (game > count){
        count = count + 1;
    }
}

var path = [ "E:\\YouTube\\Video\\Intro_Final.mp4"];
app.project.importFiles(path);
var startTimeSeconds = 0;
var endTimeSeconds = 7;
var newSubClipName = "opening";
var hasHardBoundaries = 1;
var sessionCounter = 1;
var takeVideo = 1;
var takeAudio = 1;
var projectItem = app.project.rootItem.children[1]
if ( (projectItem) && 
    ((projectItem.type == ProjectItemType.CLIP)	|| (projectItem.type == ProjectItemType.FILE)) ){
    //var newSubClipName	= prompt('Name of subclip?',	projectItem.name + '_' + sessionCounter, 'Name your subclip');
        
    var newSubClip 	= projectItem.createSubClip(newSubClipName, 
                                                    startTimeSeconds, 
                                                    endTimeSeconds, 
                                                    hasHardBoundaries,
                                                    takeVideo,
                                                    takeAudio);

    if (newSubClip){
        newSubClip.setStartTime(0); // New in 11.0
    }
    } else {
        alert("Could not sub-clip " + projectItem.name + ".");
    }
for (i = 1; i <= count; i++){
    var vid = [];
    var transition_path = [];
    i_string = i.toString();
    vid_path = file_path + "G" + i_string + "_short.mp4";
    transition = "E:\\YouTube\\Video\\game" + i_string + ".png";
    
    
   if(vid_path !== false){
       vid.push(vid_path);
       transition_path.push(transition);
       
       
       }
   app.project.importFiles(transition_path);
   app.project.importFiles(vid);
}



