using System;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionWriter : MonoBehaviour
{
    public float span = 3f;
    Encoding enc = Encoding.GetEncoding("Shift_JIS");

    void Start () {
        // 文字コードを指定

        StartCoroutine ("Logging");
    }
    
    IEnumerator Logging(){
        while (true) {
            yield return new WaitForSeconds (span);
            Debug.LogFormat ("{0}秒経過", span);
            
            // ファイルを開く
            StreamWriter writer = new StreamWriter(@"E:Samurai.txt", true, enc);
            // テキストを書き込む
            writer.WriteLine("この内容を書き込みます");

            // ファイルを閉じる
            writer.Close();
 
            Console.WriteLine("ファイルに書き込みました");
            Console.ReadKey();
        }
    }
}