function readFile(filename){
var fso = new ActiveXObject("Scripting.FileSystemObject");
var f = fso.OpenTextFile(filename,1);
var s = "";
while (!f.AtEndOfStream)
s += f.ReadLine()+"\n";
f.Close();
}
alert('AAAAAAAAAAAAAAAAAAAAAA')

