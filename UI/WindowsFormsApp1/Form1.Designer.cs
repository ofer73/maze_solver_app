
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
            this.button1 = new System.Windows.Forms.Button();
            this.Image1 = new System.Windows.Forms.PictureBox();
            this.label1 = new System.Windows.Forms.Label();
            this.startVal = new System.Windows.Forms.Label();
            this.endVal = new System.Windows.Forms.Label();
            this.start_point_radio = new System.Windows.Forms.RadioButton();
            this.end_point_radio = new System.Windows.Forms.RadioButton();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.solve_maze_button = new System.Windows.Forms.Button();
            this.imageSize = new System.Windows.Forms.Button();
            ((System.ComponentModel.ISupportInitialize)(this.Image1)).BeginInit();
            this.SuspendLayout();
            // 
            // button1
            // 
            this.button1.Cursor = System.Windows.Forms.Cursors.Hand;
            this.button1.Location = new System.Drawing.Point(16, 823);
            this.button1.Margin = new System.Windows.Forms.Padding(4);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(128, 49);
            this.button1.TabIndex = 1;
            this.button1.Text = "upload_maze";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // Image1
            // 
            this.Image1.AccessibleName = "Image";
            this.Image1.Location = new System.Drawing.Point(16, 10);
            this.Image1.Margin = new System.Windows.Forms.Padding(4);
            this.Image1.Name = "Image1";
            this.Image1.Size = new System.Drawing.Size(1562, 786);
            this.Image1.SizeMode = System.Windows.Forms.PictureBoxSizeMode.Zoom;
            this.Image1.TabIndex = 2;
            this.Image1.TabStop = false;
            this.Image1.MouseDown += new System.Windows.Forms.MouseEventHandler(this.Image1_DoubleClick);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(13, 800);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(793, 17);
            this.label1.TabIndex = 6;
            this.label1.Text = "To solve a maze. please upload a maze , then select a start and end point from th" +
    "e image. finally to start click solve my maze";
            // 
            // startVal
            // 
            this.startVal.AutoSize = true;
            this.startVal.Location = new System.Drawing.Point(284, 848);
            this.startVal.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.startVal.Name = "startVal";
            this.startVal.Size = new System.Drawing.Size(0, 17);
            this.startVal.TabIndex = 7;
            // 
            // endVal
            // 
            this.endVal.AutoSize = true;
            this.endVal.Location = new System.Drawing.Point(353, 848);
            this.endVal.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.endVal.Name = "endVal";
            this.endVal.Size = new System.Drawing.Size(0, 17);
            this.endVal.TabIndex = 8;
            // 
            // start_point_radio
            // 
            this.start_point_radio.AutoSize = true;
            this.start_point_radio.Location = new System.Drawing.Point(163, 823);
            this.start_point_radio.Margin = new System.Windows.Forms.Padding(4);
            this.start_point_radio.Name = "start_point_radio";
            this.start_point_radio.Size = new System.Drawing.Size(95, 21);
            this.start_point_radio.TabIndex = 9;
            this.start_point_radio.TabStop = true;
            this.start_point_radio.Text = "Start Point";
            this.start_point_radio.UseVisualStyleBackColor = true;
            // 
            // end_point_radio
            // 
            this.end_point_radio.AutoSize = true;
            this.end_point_radio.Location = new System.Drawing.Point(163, 851);
            this.end_point_radio.Margin = new System.Windows.Forms.Padding(4);
            this.end_point_radio.Name = "end_point_radio";
            this.end_point_radio.Size = new System.Drawing.Size(90, 21);
            this.end_point_radio.TabIndex = 10;
            this.end_point_radio.TabStop = true;
            this.end_point_radio.Text = "End Point";
            this.end_point_radio.UseVisualStyleBackColor = true;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Font = new System.Drawing.Font("Microsoft Sans Serif", 9.75F, ((System.Drawing.FontStyle)((System.Drawing.FontStyle.Bold | System.Drawing.FontStyle.Underline))), System.Drawing.GraphicsUnit.Point, ((byte)(177)));
            this.label4.Location = new System.Drawing.Point(266, 822);
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
            this.label5.Location = new System.Drawing.Point(341, 822);
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
            this.solve_maze_button.Location = new System.Drawing.Point(1396, 805);
            this.solve_maze_button.Margin = new System.Windows.Forms.Padding(4);
            this.solve_maze_button.Name = "solve_maze_button";
            this.solve_maze_button.Size = new System.Drawing.Size(155, 70);
            this.solve_maze_button.TabIndex = 13;
            this.solve_maze_button.Text = "Solve my Maze!";
            this.solve_maze_button.UseVisualStyleBackColor = false;
            this.solve_maze_button.MouseDown += new System.Windows.Forms.MouseEventHandler(this.maze_solve_button_MouseDown);
            // 
            // imageSize
            // 
            this.imageSize.Location = new System.Drawing.Point(1223, 813);
            this.imageSize.Margin = new System.Windows.Forms.Padding(4);
            this.imageSize.Name = "imageSize";
            this.imageSize.Size = new System.Drawing.Size(149, 59);
            this.imageSize.TabIndex = 14;
            this.imageSize.Text = "imageSize(test)";
            this.imageSize.UseVisualStyleBackColor = true;
            this.imageSize.Click += new System.EventHandler(this.imageSize_Click);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(1585, 885);
            this.Controls.Add(this.imageSize);
            this.Controls.Add(this.solve_maze_button);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.end_point_radio);
            this.Controls.Add(this.start_point_radio);
            this.Controls.Add(this.endVal);
            this.Controls.Add(this.startVal);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.Image1);
            this.Controls.Add(this.button1);
            this.Margin = new System.Windows.Forms.Padding(4);
            this.Name = "Form1";
            this.Text = "Maze Solver";
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.Image1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.PictureBox Image1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Label startVal;
        private System.Windows.Forms.Label endVal;
        private System.Windows.Forms.RadioButton start_point_radio;
        private System.Windows.Forms.RadioButton end_point_radio;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Button solve_maze_button;
        private System.Windows.Forms.Button imageSize;
    }
}

