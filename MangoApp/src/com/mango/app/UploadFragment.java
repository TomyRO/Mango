package com.mango.app;

import java.net.URISyntaxException;

import android.app.Activity;
import android.app.Fragment;
import android.content.Context;
import android.content.Intent;
import android.database.Cursor;
import android.net.Uri;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.View;
import android.view.View.OnClickListener;
import android.view.ViewGroup;
import android.widget.TextView;
import android.widget.Toast;

public class UploadFragment extends Fragment implements OnClickListener {

	private static final int FILE_SELECT_CODE = 0;
	private static final String TAG = UploadFragment.class.getSimpleName();
	private TextView uploadResult;
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.upload_fragment, container, false);
		view.findViewById(R.id.upload_button).setOnClickListener(this);
		uploadResult = (TextView) view.findViewById(R.id.upload_result);
		return view;
	}

	@Override
	public void onClick(View view) {
		showFileChooser();
	}
	
	@Override
	public void onActivityResult(int requestCode, int resultCode, Intent data) {
	    switch (requestCode) {
	        case FILE_SELECT_CODE:
	        if (resultCode == Activity.RESULT_OK) {
	            // Get the Uri of the selected file 
	            Uri uri = data.getData();
	            Log.d(TAG, "File Uri: " + uri.toString());
	            // Get the path
	            String path = "";
				try {
					path = getPath(getActivity(), uri);
					uploadResult.setText(path);
				} catch (URISyntaxException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
					uploadResult.setText("Problem");
				}
	            Log.d(TAG, "File Path: " + path);
	            // Get the file instance
	            // File file = new File(path);
	            // Initiate the upload
	        }
	        break;
	    }
	    super.onActivityResult(requestCode, resultCode, data);
	}

	private void showFileChooser() {
	    Intent intent = new Intent(Intent.ACTION_GET_CONTENT); 
	    intent.setType("*/*"); 
	    intent.addCategory(Intent.CATEGORY_OPENABLE);

	    try {
	        startActivityForResult(
	                Intent.createChooser(intent, "Select a File to Upload"),
	                FILE_SELECT_CODE);
	    } catch (android.content.ActivityNotFoundException ex) {
	        // Potentially direct the user to the Market with a Dialog
	        Toast.makeText(getActivity(), "Please install a File Manager.", 
	                Toast.LENGTH_SHORT).show();
	    }
	}
	
	static String getPath(Context context, Uri uri) throws URISyntaxException {
	    if ("content".equalsIgnoreCase(uri.getScheme())) {
	        String[] projection = { "_data" };
	        Cursor cursor = null;

	        try {
	            cursor = context.getContentResolver().query(uri, projection, null, null, null);
	            int column_index = cursor.getColumnIndexOrThrow("_data");
	            if (cursor.moveToFirst()) {
	            	String tmp = cursor.getString(column_index);
	                return tmp;
	            } else {
	            	return null;
	            }
	        } catch (Exception e) {
	            // Eat it
	        	Log.e("", e.getMessage());
	        	return null;
	        }
	    }
	    else if ("file".equalsIgnoreCase(uri.getScheme())) {
	        return uri.getPath();
	    } else {
	    	return null;
	    }
	} 
	
}
