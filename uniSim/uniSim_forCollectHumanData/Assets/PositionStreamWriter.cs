using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PositionStreamWriter : MonoBehaviour
{
   [SerializeField]
   string path;

   string filepath;

   public float span = 3f;

   void Start()
   {
       filepath = @"./test.txt";
       StartCoroutine ("Logging");
   }

   IEnumerator Logging(){
        while (true) {
            yield return new WaitForSeconds (span);
            Debug.LogFormat ("{0}秒経過", span);

            Vector3 p = this.transform.position;
            
            using (StreamWriter sw = new StreamWriter(filepath, true, Encoding.GetEncoding("shift_jis")))
           {
               sw.WriteLine("x:{0}, y:{1}, z:{2}",p.x, p.y, p.z);
               sw.Flush();// StreamWriterのバッファに書き出し残しがないか確認
               sw.Close();// ファイルを閉じる
           }
        }
    }
}