package org.apache.openwhisk.common
import org.apache.http.client.methods.HttpPost
import org.apache.http.entity.StringEntity
import org.apache.http.impl.client.HttpClientBuilder




object TrackLogger{
  def saveLog(data: String): Unit = {

    val url = "http://localhost:9082/logs/save-log"
    val client = HttpClientBuilder.create().build()
    val request = new HttpPost(url)

    val entity = new StringEntity(data)
    request.setEntity(entity)

    request.setHeader("Content-type", "application/json")

    client.execute(request)


  }
}

