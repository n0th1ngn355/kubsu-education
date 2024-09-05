using Npgsql;
using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace TourFirm
{
    public partial class Form1 : Form
    {
        private NpgsqlConnection con;
        private string connString =
        "Host=localhost;Username=postgres;Password=postgres;Database=Tourfirm";

        public Form1()
        {
            InitializeComponent();
            con = new NpgsqlConnection(connString);
            con.Open();
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);
            DataTable dt1 = new DataTable(), dt2 = new DataTable(), dt3 = new DataTable(), 
                dt4 = new DataTable(), dt5 = new DataTable();
            NpgsqlDataAdapter adap1 = new NpgsqlDataAdapter("SELECT * FROM customers", con),
                adap2 = new NpgsqlDataAdapter("SELECT * FROM custinfo", con),
                adap3 = new NpgsqlDataAdapter("SELECT * FROM tours", con),
                adap4 = new NpgsqlDataAdapter("SELECT * FROM seasons", con),
                adap5 = new NpgsqlDataAdapter("SELECT * FROM payments", con);
            adap1.Fill(dt1);
            adap2.Fill(dt2);
            adap3.Fill(dt3);
            adap4.Fill(dt4);
            adap5.Fill(dt5);
            dataGridView1.DataSource = dt1;
            dataGridView2.DataSource = dt2;
            dataGridView3.DataSource = dt3;
            dataGridView4.DataSource = dt4;
            dataGridView5.DataSource = dt5;
        }

        private void button1_Click(object sender, EventArgs e)
        {
            TouristsForm form2 = new TouristsForm();
            form2.ShowDialog();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            OnLoad(EventArgs.Empty);
        }
    }
}
