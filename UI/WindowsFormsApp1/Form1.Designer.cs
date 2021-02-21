
using System.Drawing;

namespace WindowsFormsApp1
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.upload_button = new System.Windows.Forms.Button();
            this.MazeImg = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.startVal = new System.Windows.Forms.Label();
            this.endVal = new System.Windows.Forms.Label();
            this.start_point_radio = new System.Windows.Forms.RadioButton();
            this.end_point_radio = new System.Windows.Forms.RadioButton();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.solve_maze_button = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.sizeTest = new System.Windows.Forms.Button();
            this.solvedFlag = new System.Windows.Forms.Label();
            ((System.ComponentModel.ISupportInitialize)(this.MazeImg)).BeginInit();
            this.SuspendLayout();
            // 
            // upload_button
            // 
            this.upload_button.Cursor = System.Windows.Forms.Cursors.Hand;
            this.upload_button.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.upload_button.ForeColor = System.Drawing.Color.Fuchsia;
            this.upload_button.Location = new System.Drawing.Point(7, 744);
            this.upload_button.Margin = new System.Windows.Forms.Padding(4);
            this.upload_button.Name = "upload_button";
            this.upload_button.Size = new System.Drawing.Size(119, 49);
            this.upload_button.TabIndex = 1;
            this.upload_button.Text = "Upload Maze";
            this.upload_button.UseVisualStyleBackColor = true;
            this.upload_button.Click += new System.EventHandler(this.uploadButtonClick);
            // 
            // MazeImg
            // 
            this.MazeImg.AccessibleName = "Image";
            this.MazeImg.Location = new System.Drawing.Point(16, 10);
            this.MazeImg.Margin = new System.Windows.Forms.Padding(4);
            this.MazeImg.Name = "MazeImg";
            this.MazeImg.Size = new System.Drawing.Size(1441, 702);
            this.MazeImg.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.MazeImg.TabIndex = 2;
            this.MazeImg.TabStop = false;
            this.MazeImg.MouseDown += new System.Windows.Forms.MouseEventHandler(this.MazeImg_DoubleClick);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label1.Location = new System.Drawing.Point(414, 744);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(776, 18);
            this.label1.TabIndex = 6;
            this.label1.Text = "To solve a maze. please upload a maze , select start and end point inside the maz" +
    "e, and finally click the green button! ";
            // 
            // startVal
            // 
            this.startVal.AutoSize = true;
            this.startVal.Font = new System.Drawing.Font("Microsoft Sans Serif", 9F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.startVal.Location = new System.Drawing.Point(241, 768);
            this.startVal.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.startVal.Name = "startVal";
            this.startVal.Size = new System.Drawing.Size(0, 18);
            this.startVal.TabIndex = 7;
            // 
            // endVal
            // 
            this.endVal.AutoSize = true;
            this.endVal.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.endVal.Location = new System.Drawing.Point(331, 770);
            this.endVal.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.endVal.Name = "endVal";
            this.endVal.Size = new System.Drawing.Size(0, 17);
            this.endVal.TabIndex = 8;
            // 
            // start_point_radio
            // 
            this.start_point_radio.AutoSize = true;
            this.start_point_radio.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.start_point_radio.Location = new System.Drawing.Point(134, 745);
            this.start_point_radio.Margin = new System.Windows.Forms.Padding(4);
            this.start_point_radio.Name = "start_point_radio";
            this.start_point_radio.Size = new System.Drawing.Size(106, 21);
            this.start_point_radio.TabIndex = 9;
            this.start_point_radio.TabStop = true;
            this.start_point_radio.Text = "Start Point";
            this.start_point_radio.UseVisualStyleBackColor = true;
            // 
            // end_point_radio
            // 
            this.end_point_radio.AutoSize = true;
            this.end_point_radio.Font = new System.Drawing.Font("Microsoft Sans Serif", 7.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.end_point_radio.Location = new System.Drawing.Point(134, 773);
            this.end_point_radio.Margin = new System.Windows.Forms.Padding(4);
            this.end_point_radio.Name = "end_point_radio";
            this.end_point_radio.Size = new System.Drawing.Size(99, 21);
            this.end_point_radio.TabIndex = 10;
            this.end_point_radio.TabStop = true;
            this.end_point_radio.Text = "End Point";
            this.end_point_radio.UseVisualStyleBackColor = true;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Underline))), System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label4.ForeColor = System.Drawing.Color.Red;
            this.label4.Location = new System.Drawing.Point(258, 744);
            this.label4.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(50, 20);
            this.label4.TabIndex = 11;
            this.label4.Text = "Start";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Underline))), System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label5.ForeColor = System.Drawing.Color.Blue;
            this.label5.Location = new System.Drawing.Point(341, 745);
            this.label5.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(41, 20);
            this.label5.TabIndex = 12;
            this.label5.Text = "End";
            // 
            // solve_maze_button
            // 
            this.solve_maze_button.BackColor = System.Drawing.Color.Lime;
            this.solve_maze_button.Font = new System.Drawing.Font("Microsoft Sans Serif", 11.25F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.solve_maze_button.ForeColor = System.Drawing.Color.Blue;
            this.solve_maze_button.Location = new System.Drawing.Point(1302, 724);
            this.solve_maze_button.Margin = new System.Windows.Forms.Padding(4);
            this.solve_maze_button.Name = "solve_maze_button";
            this.solve_maze_button.Size = new System.Drawing.Size(155, 70);
            this.solve_maze_button.TabIndex = 13;
            this.solve_maze_button.Text = "Solve my Maze!";
            this.solve_maze_button.UseVisualStyleBackColor = false;
            this.solve_maze_button.MouseDown += new System.Windows.Forms.MouseEventHandler(this.MazeSolveButtonMouseDown);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.Color.FromArgb(((int)(((byte)(255)))), ((int)(((byte)(255)))), ((int)(((byte)(128)))));
            this.label2.Font = new System.Drawing.Font("Microsoft Sans Serif", 10.8F, System.Drawing.FontStyle.Bold, System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label2.ForeColor = System.Drawing.Color.FromArgb(((int)(((byte)(192)))), ((int)(((byte)(0)))), ((int)(((byte)(0)))));
            this.label2.Location = new System.Drawing.Point(413, 768);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(683, 24);
            this.label2.TabIndex = 14;
            this.label2.Text = "IMPORTANT! please choose 2 points Inside the maze! (not background)";
            // 
            // sizeTest
            // 
            this.sizeTest.Location = new System.Drawing.Point(1207, 744);
            this.sizeTest.Name = "sizeTest";
            this.sizeTest.Size = new System.Drawing.Size(75, 49);
            this.sizeTest.TabIndex = 15;
            this.sizeTest.Text = "sizeTest";
            this.sizeTest.UseVisualStyleBackColor = true;
            this.sizeTest.Visible = false;
            this.sizeTest.Click += new System.EventHandler(this.sizeTest_Click);
            // 
            // solvedFlag
            // 
            this.solvedFlag.AutoSize = true;
            this.solvedFlag.Location = new System.Drawing.Point(1262, 724);
            this.solvedFlag.Name = "solvedFlag";
            this.solvedFlag.Size = new System.Drawing.Size(16, 17);
            this.solvedFlag.TabIndex = 17;
            this.solvedFlag.Text = "0";
            this.solvedFlag.Visible = false;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1471, 800);
            this.Controls.Add(this.solvedFlag);
            this.Controls.Add(this.sizeTest);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.solve_maze_button);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.end_point_radio);
            this.Controls.Add(this.start_point_radio);
            this.Controls.Add(this.endVal);
            this.Controls.Add(this.startVal);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.MazeImg);
            this.Controls.Add(this.upload_button);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "Form1";
            this.Text = "Maze Solver";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            ((System.ComponentModel.ISupportInitialize)(this.MazeImg)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button upload_button;
        private System.Windows.Forms.PictureBox MazeImg;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label startVal;
        private System.Windows.Forms.Label endVal;
        private System.Windows.Forms.RadioButton start_point_radio;
        private System.Windows.Forms.RadioButton end_point_radio;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button solve_maze_button;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.Button sizeTest;
        private System.Windows.Forms.Label solvedFlag;
    }
}

