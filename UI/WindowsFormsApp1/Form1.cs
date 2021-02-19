using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.Drawing;
using System.Diagnostics;
using IronPython.Hosting;
using System.IO;

namespace WindowsFormsApp1
{

    public partial class Form1 : Form
    {

        public Form1()
        {
            InitializeComponent();
        }

        private void uploadButtonClick(object sender, EventArgs e)
        {
            try
            {
                OpenFileDialog dialog = new OpenFileDialog();
                dialog.Filter = "jpg files (*.jpg)|*.jpg|jpeg files (*.jpeg)|*.jpeg| PNG files |*.png| All Files(*.*)|*.*";

                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK){
                    var imageLocation = dialog.FileName;
                    Image1.ImageLocation = imageLocation;
                    startVal.Text = "";
                    endVal.Text = "";
                }
            }
            catch
            {
                MessageBox.Show("Invalid Image","Error",MessageBoxButtons.OK,MessageBoxIcon.Error);
            }
        }

        private void Image1_DoubleClick(object sender, MouseEventArgs e)
        {
            if (Image1.Image != null)
            {
                var b = Image1;
                int x = b.Width * e.X / Image1.Width;
                int y = b.Height * e.Y / Image1.Height;
                var Size = getNewImageSize();
                x -= ((Image1.Width - Size.Width) / 2); // decrease the gap between imagebox and the actual image
                y -= ((Image1.Height - Size.Height) / 2);

                if (!end_point_radio.Checked && !start_point_radio.Checked)
                        MessageBox.Show(String.Format("X={0}, Y={1}, please choose start or end point to update one of them", x, y));
                    else if (start_point_radio.Checked)
                    {
                        startVal.Text = String.Format("({0},{1})", x, y);
                    }
                    else
                    {
                        endVal.Text = String.Format("({0},{1})", x, y);
                    }
            }
            else 
            {
                MessageBox.Show(String.Format("No maze uploaded, please choose a maze!"));
            }

        }

        private void maze_solve_button_MouseDown(object sender, MouseEventArgs e)
        {
            if(startVal.Text.Length>0 && endVal.Text.Length > 0 && Image1.Image!=null)
            {

                //Proccess args
                var start = startVal.Text.Substring(1, startVal.Text.Length - 2); // Remove parenthasis ()
                var end = endVal.Text.Substring(1, endVal.Text.Length - 2);
                var filppedStart = string.Join(",",start.Split(',').Reverse());
                var filppedEnd = string.Join(",", end.Split(',').Reverse());
                var imagePath = Image1.ImageLocation;
                var imageNewSize = getNewImageSize();
                var sizeParam = $"{imageNewSize.Height},{imageNewSize.Width}";

                var cmds = new List<string> 
                { 
                    "pip install -r requirements.txt",
                    $"python solve_maze.py {filppedStart} {filppedEnd} {imagePath} {sizeParam}"
                };

                RunCommands(cmds);

            }
            else if(Image1.Image!=null)
            {
                MessageBox.Show("You Must enter Start and End Points before solving the maze!");
            }
            else
            {
                MessageBox.Show("please upload a maze!");
            }
        }

        private void imageSize_Click(object sender, EventArgs e)
        {
            if (Image1.Image == null)
                MessageBox.Show("no image cuurently uploade");
            else
            {
                Size imageSize = getNewImageSize();
                MessageBox.Show($"{imageSize}");
            }
        }

        private Size getNewImageSize() // get the size of the actual image on the picture box (zoom mode maintains ratio of original image)
        {
            var img = Image1.Image;
            var wfactor = (double)img.Width / Image1.Width;
            var hfactor = (double)img.Height / Image1.Height;

            var resizeFactor = Math.Max(wfactor, hfactor);
            var imageSize = new Size((int)(img.Width / resizeFactor), (int)(img.Height / resizeFactor));
            return imageSize;
        }

        private static void RunCommands(List<string> cmds)
        {
            var process = new Process();
            var psi = new ProcessStartInfo();
            psi.FileName = "cmd.exe";
            psi.RedirectStandardInput = true;
            psi.RedirectStandardOutput = true;
            psi.RedirectStandardError = true;
            psi.UseShellExecute = false;
            var currDir = Directory.GetCurrentDirectory();
            var indexOfScriptPath = currDir.LastIndexOf(@"\UI\");
            psi.WorkingDirectory = currDir.Substring(0, indexOfScriptPath);
            process.StartInfo = psi;
            process.Start();
            process.OutputDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
            process.ErrorDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            using (StreamWriter sw = process.StandardInput)
            {
                foreach (var cmd in cmds)
                {
                    sw.WriteLine(cmd);
                    
                }
            }
            process.WaitForExit();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }

        private void label2_Click(object sender, EventArgs e)
        {

        }

        private void sizeTest_Click(object sender, EventArgs e)
        {
            if (Image1.Image != null)
            {
                var size = getNewImageSize();
                MessageBox.Show($"Height: {size.Height} Width: {size.Width}");
            }
        }
    }
}
