var meta_file = File.openDialog("Selection prompt");
var meta_string = meta_file.toString();
var file_length = meta_string.lastIndexOf("/") + 1;
var file_path = meta_string.substr(0,file_length)
for (i = 0; i < 5; i++){
    i_string = i.toString();
    vid_path = file_path + "g" + i_string + "_short.mp4";
   if(vid_path !== false){
       transition = "E:\\YouTube\\Video\\game" + i_string + ".mp4";
       app.project.importFiles(vid_path);
       app.project.importFiles(transition);
       }
}

var path = [file_path + "G1_short", file_path + "G2_short", file_path + "G3_short", file_path + "G4_short", file_path + "G5_short"];

app.project.createNewSequence("test","C:\\Program Files\\Adobe\\Adobe Premiere Pro CC 2017\\Settings\\SequencePresets\\ARRI\\1080p\\ARRI 1080p 30fps.sqpreset", 0)