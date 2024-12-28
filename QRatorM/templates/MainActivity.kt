package com.example.qrator

import android.Manifest
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.os.Bundle
import android.os.Environment
import android.os.StrictMode
import android.widget.Button
import android.widget.EditText
import android.widget.Toast
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.zxing.BarcodeFormat
import com.google.zxing.WriterException
import com.google.zxing.integration.android.IntentIntegrator
import com.google.zxing.integration.android.IntentResult
import com.journeyapps.barcodescanner.BarcodeEncoder
import java.io.File
import java.io.FileOutputStream
import java.io.OutputStreamWriter
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : AppCompatActivity() {

    private var ipAddress: String? = null
    private var scannedUrl: String? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)


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

        findViewById<Button>(R.id.btn_create_qr).setOnClickListener {
            createQR()
        }


        if (ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.WRITE_EXTERNAL_STORAGE), 1)
        }
    }

    private fun startQRScanner() {
        val integrator = IntentIntegrator(this)
        integrator.setDesiredBarcodeFormats(IntentIntegrator.QR_CODE)
        integrator.setPrompt("Scan a QR Code")
        integrator.setCameraId(0)  // camera
        integrator.setBeepEnabled(true)  // sound q
        integrator.setBarcodeImageEnabled(true)  // save code
        integrator.initiateScan()  // start qr scan
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

    private fun createQR() {
        val ip = ipAddress

        if (ip == null) {
            Toast.makeText(this, "Please insert an IP address first", Toast.LENGTH_LONG).show()
            return
        }

        val qrContent = "http://$ip:5000"
        val barcodeEncoder = BarcodeEncoder()

        try {
            val bitmap = barcodeEncoder.encodeBitmap(qrContent, BarcodeFormat.QR_CODE, 400, 400)

            val filePath = File(Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_PICTURES), "qr_code.png")
            val outputStream = FileOutputStream(filePath)

            bitmap.compress(Bitmap.CompressFormat.PNG, 100, outputStream)
            outputStream.flush()
            outputStream.close()

            Toast.makeText(this, "QR Code saved to Pictures/qr_code.png", Toast.LENGTH_LONG).show()
        } catch (e: WriterException) {
            Toast.makeText(this, "Error creating QR code: ${e.message}", Toast.LENGTH_LONG).show()
        } catch (e: Exception) {
            Toast.makeText(this, "Error saving QR code: ${e.message}", Toast.LENGTH_LONG).show()
        }
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

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 1) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                Toast.makeText(this, "Permission granted!", Toast.LENGTH_SHORT).show()
            } else {
                Toast.makeText(this, "Permission denied!", Toast.LENGTH_SHORT).show()
            }
        }
    }
}
