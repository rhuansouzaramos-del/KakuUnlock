package com.kaku.unlock
import android.os.Bundle
import android.widget.Button
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import java.io.DataOutputStream

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val button = Button(this).apply {
            text = "INICIAR BROM MODE"
            setOnClickListener {
                if (executeRootCommand("reboot edl") || executeRootCommand("reboot -p")) {
                    Toast.makeText(this@MainActivity, "Reiniciando para BROM...", Toast.LENGTH_LONG).show()
                } else {
                    Toast.makeText(this@MainActivity, "Falha no Root!", Toast.LENGTH_SHORT).show()
                }
            }
        }
        setContentView(button)
    }
    private fun executeRootCommand(command: String): Boolean {
        return try {
            val process = Runtime.getRuntime().exec("su")
            val os = DataOutputStream(process.outputStream)
            os.writeBytes("$command\n"); os.writeBytes("exit\n"); os.flush()
            process.waitFor() == 0
        } catch (e: Exception) { false }
    }
}
