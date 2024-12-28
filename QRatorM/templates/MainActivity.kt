package com.example.qrator

import android.content.Intent
import android.os.Bundle
import android.os.StrictMode
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private var ipAddress: String? = null
    private var scannedUrl: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Για να επιτρέψεις τις λειτουργίες δικτύου στο κύριο νήμα (μόνο για δοκιμές, όχι για παραγωγή)
        StrictMode.setThreadPolicy(StrictMode.ThreadPolicy.Builder().permitAll().build())

        findViewById<Button>(R.id.btn_scan_qr).setOnClickListener {
            startQRScanner()
        }

        findViewById<Button>(R.id.btn_insert_ip).setOnClickListener {
            showInsertIpDialog()
        }

        findViewById<Button>(R.id.btn_run_script).setOnClickListener {
            runScript()
        }
    }

    private fun startQRScanner() {
        val integrator = IntentIntegrator(this)
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
        integrator.setPrompt("Scan a QR Code")
        integrator.setCameraId(0)  // Χρησιμοποίησε συγκεκριμένη κάμερα (μπροστά ή πίσω)
        integrator.setBeepEnabled(true)  // Παίζει ήχο όταν σαρωθεί ένας QR κωδικός
        integrator.setBarcodeImageEnabled(true)  // Αποθηκεύει την εικόνα του σαρωμένου κωδικού
        integrator.initiateScan()  // Ξεκινά τον σαρωτή QR κωδικών
    }

    private fun showInsertIpDialog() {
        val builder = AlertDialog.Builder(this)
        builder.setTitle("Insert IP")

        // Set up the input
        val input = EditText(this)
        builder.setView(input)

        // Set up the buttons
        builder.setPositiveButton("OK") { dialog, which ->
            ipAddress = input.text.toString()
            // Εδώ μπορείς να κάνεις οτιδήποτε με το αποθηκευμένο IP
        }
        builder.setNegativeButton("Cancel") { dialog, which ->
            dialog.cancel()
        }

        builder.show()
    }

    private fun runScript() {
        val url = scannedUrl
        val ip = ipAddress

        if (url == null || ip == null) {
            Toast.makeText(this, "Please scan a QR code and insert an IP address first", Toast.LENGTH_LONG).show()
            return
        }

        val jsonInputString = """{"url": "$url"}"""
        val postUrl = "http://$ip:5000/run_script"

        Thread {
            try {
                val urlObj = URL(postUrl)
                val conn = urlObj.openConnection() as HttpURLConnection
                conn.requestMethod = "POST"
                conn.setRequestProperty("Content-Type", "application/json; utf-8")
                conn.setRequestProperty("Accept", "application/json")
                conn.doOutput = true

                OutputStreamWriter(conn.outputStream).use { writer ->
                    writer.write(jsonInputString)
                }

                val responseCode = conn.responseCode
                runOnUiThread {
                    if (responseCode == 200) {
                        Toast.makeText(this, "Script executed successfully", Toast.LENGTH_LONG).show()
                    } else {
                        Toast.makeText(this, "Failed to execute script: $responseCode", Toast.LENGTH_LONG).show()
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                }
            }
        }.start()
    }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        super.onActivityResult(requestCode, resultCode, data)

        val result: IntentResult? = IntentIntegrator.parseActivityResult(requestCode, resultCode, data)
        result?.let {
            if (it.contents == null) {
                // Ο χρήστης ακύρωσε τη σάρωση
            } else {
                // Επιτυχής σάρωση QR κωδικού
                scannedUrl = it.contents
                // Εδώ μπορείς να κάνεις οτιδήποτε με το αποτέλεσμα της σάρωσης
            }
        }
    }
}
