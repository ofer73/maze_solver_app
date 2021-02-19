﻿using System;
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

        private void button1_Click(object sender, EventArgs e)
        {
            try
            {
                OpenFileDialog dialog = new OpenFileDialog();
                dialog.Filter = "jpg files (*.jpg|*.jpg| PNG files |*.png| All Files(*.*)|*.*";

                if (dialog.ShowDialog() == System.Windows.Forms.DialogResult.OK){
                    var imageLocation = dialog.FileName;
                    Image1.ImageLocation = imageLocation;
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
                var Size = getNewImageSIze();
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
            MessageBox.Show(String.Format("No maze uploaded, please choose a maze!"));

        }

        private void maze_solve_button_MouseDown(object sender, MouseEventArgs e)
        {
            if(startVal.Text.Length>0 && endVal.Text.Length > 0 && Image1.Image!=null)
            {
                
                ////proccess Info
                //var psi = new ProcessStartInfo();
                //psi.FileName = @"C:\Users\t-ofermoses\Anaconda3\python.exe";
                //var script = @"C:\Users\t-ofermoses\OneDrive - Microsoft\Desktop\Ofer\Univesity\SemesterE\CV\assignments\maze_solver\maze_solver\main_eg.py";

                //Proccess args
                var start = startVal.Text.Substring(1, startVal.Text.Length - 2); // Remove parenthasis ()
                var end = endVal.Text.Substring(1, endVal.Text.Length - 2);
                var filppedStart = string.Join(",",start.Split(',').Reverse());
                var filppedEnd = string.Join(",", end.Split(',').Reverse());
                var imagePath = Image1.ImageLocation;
                var imageNewSize = getNewImageSIze();
                var sizeParam = $"{imageNewSize.Height},{imageNewSize.Width}";

                var cmds = new List<string> 
                { 
                    "conda create maze_solver_env",
                    "conda activate maze_solver_env",
                    "pip install -r requirements.txt",
                    $"python solve_maze.py {filppedStart} {filppedEnd} {imagePath} {sizeParam}"
                };

                RunCommands(cmds);


                //psi.Arguments = $"\"{script}\" \"{start_int}\" \"{end_int}\" \"{Image1.Image}\"";
                ////psi.Arguments = $"\"{script}\""; // working examplk

                ////prccess configuration
                //psi.UseShellExecute = false;
                //psi.CreateNoWindow = true;
                //psi.RedirectStandardOutput = true;
                //psi.RedirectStandardError = true;

                ////excecute
                //var errors = "";
                //var results = "";

                //using (var process = Process.Start(psi))
                //{
                //    errors = process.StandardError.ReadToEnd();
                //    results = process.StandardOutput.ReadToEnd();
                //    //if (results != null)
                //    //{
                //    //    Process photoViewer = new Process();
                //    //    photoViewer.StartInfo.FileName = @"The photo viewer file path";
                //    //    photoViewer.StartInfo.Arguments = @"Your image file path";
                //    //    photoViewer.Start();
                //    //}

                //}
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
                Size imageSize = getNewImageSIze();
                MessageBox.Show($"{imageSize}");
            }
        }

        private Size getNewImageSIze() // get the size of the actual image on the picture box (zoom mode maintains ratio of original image)
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
            //process.OutputDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
            //process.ErrorDataReceived += (sender, e) => { Console.WriteLine(e.Data); };
            //process.BeginOutputReadLine();
            //process.BeginErrorReadLine();

            using (StreamWriter sw = process.StandardInput)
            {
                foreach (var cmd in cmds)
                {
                    sw.WriteLine(cmd);
                    var error = process.StandardError.ReadToEnd();
                    var result = process.StandardError.ReadToEnd();
                }
            }
            process.WaitForExit();
        }

        private void Form1_Load(object sender, EventArgs e)
        {

        }
    }
}
