
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
    var count_string = count.toString();
    if (meta_data["infographics"][i].substr(0,2) == "G" + count_string){
        count = count + 1;
    }
}

for (i = 1; i < count; i++){
    var paths = [];   
    i_string = i.toString();
    vid_path = file_path + "G" + i_string + "_short.mp4";
    transition = "E:\\YouTube\\Video\\game" + i_string + ".png";
    
    
   if(vid_path !== false){
       paths.push(vid_path);
       paths.push(transition);
       
       
       }
   app.project.importFiles(paths);
}



