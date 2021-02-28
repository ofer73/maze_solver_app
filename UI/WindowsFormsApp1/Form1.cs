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
        private Graphics _pictureBoxGraphics;
        private Pen _startPen = new Pen(Color.Red);
        private Pen _endPen = new Pen(Color.Blue);
        private Brush _startBrush = new SolidBrush(Color.Red);
        private Brush _endBrush = new SolidBrush(Color.Blue);
        private string imgLocation;
        private (int, int) pictureBoxStartPoint = (-1, -1);
        private (int, int) pictureBoxEndPoint = (-1, -1);
        private readonly List<string> _supportedImageFormats = new List<string> {".jpg",".jpeg",".png"};

        public Form1()
        {
            InitializeComponent();
    }

        private void uploadButtonClick(object sender, EventArgs e)
        {
            try
            {
                OpenFileDialog dialog = new OpenFileDialog();
                dialog.Filter = "jpg files (*.jpg)|*.jpg|jpeg files (*.jpeg)|*.jpeg|png files (*.png)|*.png| All Files(*.*)|*.*";

                if (dialog.ShowDialog() == DialogResult.OK)
                {
                    var fileName = dialog.FileName;
                    if(_supportedImageFormats.Any(fileSuffix => fileName.EndsWith(fileSuffix)) && !fileName.Contains(';'))
                    {
                        pictureBoxEndPoint = (-1, -1);
                        pictureBoxStartPoint = (-1, -1);
                        imgLocation = dialog.FileName;
                        MazeImg.ImageLocation = imgLocation;
                        startVal.Text = "";
                        endVal.Text = "";
                    }
                    else
                    {
                        if (fileName.Contains(';'))
                        {
                            MessageBox.Show("Invalid File Path\nPath must not contain SemiColon!(;)", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                        else
                        {
                            MessageBox.Show("Invalid Image\nPlease upload only in jpg/jpeg/png format!", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                        }
                    }
                }
            }
            catch
            {
                MessageBox.Show("Invalid Image", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void MazeImg_DoubleClick(object sender, MouseEventArgs e)
        {
            if (MazeImg.Image != null)
            {
                _pictureBoxGraphics = MazeImg.CreateGraphics();
                var b = MazeImg;
                int x = b.Width * e.X / MazeImg.Width;
                int y = b.Height * e.Y / MazeImg.Height;
                var Size = getNewImageSize();
                x -= ((MazeImg.Width - Size.Width) / 2); // decrease the gap between imagebox and the actual image
                y -= ((MazeImg.Height - Size.Height) / 2);

                if (!end_point_radio.Checked && !start_point_radio.Checked)
                    MessageBox.Show(String.Format("X={0}, Y={1}, please choose start or end point to update one of them", x, y));
                else if (start_point_radio.Checked)
                {
                    startVal.Text = String.Format("({0},{1})", x, y);
                    pictureBoxStartPoint = (e.X, e.Y);
                    MazeImg.Refresh();
                    if(pictureBoxEndPoint.Item1 >-1 && pictureBoxEndPoint.Item2 > -1)
                    {
                        _pictureBoxGraphics.DrawEllipse(_endPen, pictureBoxEndPoint.Item1-5, pictureBoxEndPoint.Item2-5, 6, 6);
                        _pictureBoxGraphics.FillEllipse(_endBrush, pictureBoxEndPoint.Item1-5, pictureBoxEndPoint.Item2-5, 6, 6);
                    }
                    _pictureBoxGraphics.DrawEllipse(_startPen, e.X-5, e.Y-5, 6, 6);
                    _pictureBoxGraphics.FillEllipse(_startBrush, e.X-5, e.Y-5, 6, 6);

                }
                else
                {
                    endVal.Text = String.Format("({0},{1})", x, y);
                    pictureBoxEndPoint = (e.X, e.Y);
                    MazeImg.Refresh();
                    if (pictureBoxStartPoint.Item1 > -1 && pictureBoxStartPoint.Item2 > -1)
                    {
                        _pictureBoxGraphics.DrawEllipse(_startPen, pictureBoxStartPoint.Item1-5, pictureBoxStartPoint.Item2-5, 6, 6);
                        _pictureBoxGraphics.FillEllipse(_startBrush, pictureBoxStartPoint.Item1-5, pictureBoxStartPoint.Item2-5, 6, 6);

                    }
                    _pictureBoxGraphics.DrawEllipse(_endPen, e.X-5, e.Y - 5, 6, 6);
                    _pictureBoxGraphics.FillEllipse(_endBrush, e.X-5, e.Y - 5, 6, 6);
                }
            }
            else
            {
                MessageBox.Show(String.Format("No maze uploaded, please choose a maze!"));
            }

        }

        private void MazeSolveButtonMouseDown(object sender, MouseEventArgs e)
        {
            if (startVal.Text.Length > 0 && endVal.Text.Length > 0 && MazeImg.Image != null)
            {
                if(solvedFlag.Text == "0")
                {
                    if (MessageBox.Show("Please approve installing requirement modules for your default python interpeter\nOpenCV,numpy... (See requirements.txt for specifics)", "Maze Solver",
                    MessageBoxButtons.YesNo) == DialogResult.Yes)
                    {
                        runInstallRequirements();
                        solvedFlag.Text = "1";
                    }
                    else
                    {
                        MessageBox.Show("Solving may Fail due to missing packages!");
                    }
                }

                //Proccess args
                var start = startVal.Text.Substring(1, startVal.Text.Length - 2); // Remove parenthasis ()
                var end = endVal.Text.Substring(1, endVal.Text.Length - 2);
                var filppedStart = string.Join(",", start.Split(',').Reverse());
                var filppedEnd = string.Join(",", end.Split(',').Reverse());
                var imagePath = MazeImg.ImageLocation;
                var imageNewSize = getNewImageSize();
                var sizeParam = $"{imageNewSize.Height},{imageNewSize.Width}";
                var replacedImagePath = imagePath.Replace(" ", ";");    // Replace whitespace with semi colon for valid params read

                // Run Solving python script
                var solveCommand = $"python solve_maze.py {filppedStart} {filppedEnd} {replacedImagePath} {sizeParam}";
                var result = runMazeSolver(solveCommand);

                if (string.IsNullOrEmpty(result) || result.StartsWith("Failed"))
                {
                    if (result.EndsWith("1"))
                    {
                        MessageBox.Show("Solving the maze Failed because start or end points were not inside the maze \n please choose new points!");
                    }
                    else if (result.EndsWith("2"))
                    {
                        MessageBox.Show("Solving the maze Failed - unable to open image\n(name could be invalid, please do not uses Whitespace)");
                    }
                    else
                    {
                        MessageBox.Show("Solving the maze Failed!");
                    }
                }
                else
                {
                    solvedFlag.Text = "1";
                    using (var process = Process.Start($"{getMainDirectoryPath()}\\mazes\\tmp_solved\\{result}"))
                    {
                    }
                }
            }
            else if (MazeImg.Image != null)
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
            if (MazeImg.Image == null)
                MessageBox.Show("no image cuurently uploade");
            else
            {
                Size imageSize = getNewImageSize();
                MessageBox.Show($"{imageSize}");
            }
        }

        // get the size of the actual image on the picture box (zoom mode maintains ratio of original image)
        private Size getNewImageSize() 
        {
            var img = MazeImg.Image;
            var wfactor = (double)img.Width / MazeImg.Width;
            var hfactor = (double)img.Height / MazeImg.Height;

            var resizeFactor = Math.Max(wfactor, hfactor);
            var imageSize = new Size((int)(img.Width / resizeFactor), (int)(img.Height / resizeFactor));
            return imageSize;
        }

        private static void runInstallRequirements()
        {
            var command = "pip install -r requirements.txt";
            ProcessStartInfo startInfo = new ProcessStartInfo();
            startInfo.WorkingDirectory = getMainDirectoryPath();
            startInfo.UseShellExecute = false;
            startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            startInfo.FileName = "cmd.exe";
            startInfo.RedirectStandardInput = true;
            using (var procces = Process.Start(startInfo))
            {
                using (StreamWriter sw = procces.StandardInput)
                {
                    sw.WriteLine(command);
                }
                procces.WaitForExit();
            }
        }

        private static string runMazeSolver(string command)
        {
            var startInfo = new ProcessStartInfo();
            startInfo.WorkingDirectory = getMainDirectoryPath();
            startInfo.WindowStyle = System.Diagnostics.ProcessWindowStyle.Hidden;
            startInfo.FileName = "cmd.exe";
            startInfo.UseShellExecute = false;
            //startInfo.CreateNoWindow = true;
            startInfo.RedirectStandardInput = true;
            startInfo.RedirectStandardOutput = true;
            startInfo.RedirectStandardError = true;

            // execute
            var errors = "";
            var output = "";
            using(var procces = Process.Start(startInfo))
            {
                using (StreamWriter sw = procces.StandardInput)
                {
                    sw.WriteLine(command);
                }

                errors = procces.StandardError.ReadToEnd();
                output = procces.StandardOutput.ReadToEnd();
            }

            // Parse output to find results of solving process
            var getOutSplit = output.Split('*');
            if (getOutSplit.Length > 2)
            {
                return getOutSplit[1];
            }

            Console.WriteLine("Errors ; ");
            Console.WriteLine(errors);
            return string.Empty;
        }

        private static string getMainDirectoryPath()
        {
            var currDir = Directory.GetCurrentDirectory();
            var indexOfScriptPath = currDir.LastIndexOf(@"\UI\");
            var homeDir = currDir.Substring(0, indexOfScriptPath);
            return homeDir;
        }

        private void sizeTest_Click(object sender, EventArgs e)
        {
            if (MazeImg.Image != null)
            {
                var size = getNewImageSize();
                MessageBox.Show($"Height: {size.Height} Width: {size.Width}");
            }
        }


        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            if(MessageBox.Show("Sure You want to exit?\n(all unsaved solutions on temp folder will be lost)","Maze Solver",
                MessageBoxButtons.YesNo) == DialogResult.Yes)
            {
                deleteTempFiles();
            }
            else
            {
                e.Cancel = true;
            }
        }

        private void deleteTempFiles()
        {
            var homeDir = getMainDirectoryPath();
            var deletePath = $"{homeDir}\\mazes\\tmp_solved";
            System.IO.DirectoryInfo di = new DirectoryInfo(deletePath);

            foreach (FileInfo file in di.GetFiles())
            {
                file.Delete();
            }
        }
    }
}
