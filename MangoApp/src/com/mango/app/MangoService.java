package com.mango.app;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

import com.google.gson.Gson;
import com.google.gson.JsonArray;
import com.google.gson.JsonParser;
import com.squareup.okhttp.MediaType;
import com.squareup.okhttp.OkHttpClient;
import com.squareup.okhttp.Request;
import com.squareup.okhttp.RequestBody;
import com.squareup.okhttp.Response;

public class MangoService {
	
	private final String BASE_URL = "";
	private final String GET_FILES_URL = "/get_files";
	private final String DOWNLOAD_URL = "/download";
	private final String UPLOAD_URL = "/upload";
	
	 public static final MediaType MEDIA_TYPE_MARKDOWN
     	= MediaType.parse("application/octet-stream");
	
	private OkHttpClient client = new OkHttpClient();
	
	public MangoService() {
		
	}
	
	public List<String> fetchFilesNames() {
		Request request = new Request.Builder()
	      .url(BASE_URL + GET_FILES_URL)
	      .build();

		List<String> result = new ArrayList<String>();
		
		try {
			Response response = client.newCall(request).execute();
			
			JsonArray array = new JsonParser().parse(response.body().string())
					.getAsJsonArray();
			
			for (int i=0;i<array.size();i++) {
				String str = array.get(i).getAsString();
				result.add(str);
			}
			
			return result;
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	 
	}
	
	
	public boolean uploadFile(File f) {
		Request request = new Request.Builder()
			.url(BASE_URL + UPLOAD_URL)
			.post(RequestBody.create(MEDIA_TYPE_MARKDOWN, f))
			.build();
		
		try {
			Response response = client.newCall(request).execute();
			
			if (!response.isSuccessful())
				throw new IOException("Unexpected code " + response);
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		return true;
	}
}
