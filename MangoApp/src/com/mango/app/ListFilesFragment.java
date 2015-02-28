package com.mango.app;

import android.app.Fragment;
import android.os.Bundle;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.BaseAdapter;
import android.widget.ListView;
import android.widget.TextView;

public class ListFilesFragment extends Fragment {
	
	private ListView filesListView;
	private String[] files = {"File1", "File2", "File3", "File4"};
	
	@Override
	public View onCreateView(LayoutInflater inflater, ViewGroup container,
			Bundle savedInstanceState) {
		View view = inflater.inflate(R.layout.show_files_fragment, container, false);
		filesListView = (ListView) view.findViewById(R.id.files_list);
		filesListView.setAdapter(new FilesListAdapter());
		return view;
	}
	
	private class FilesListAdapter extends BaseAdapter {

		@Override
		public int getCount() {
			return files.length;
		}

		@Override
		public Object getItem(int position) {
			return files[position];
		}

		@Override
		public long getItemId(int position) {
			return position;
		}

		@Override
		public View getView(int position, View convertView, ViewGroup container) {
			View view = LayoutInflater.from(getActivity()).inflate(R.layout.file_list_item, null);
			
			TextView textView = (TextView) view.findViewById(R.id.file_name);
			textView.setText(String.valueOf(getItem(position)));
			
			return view;
		}
		
	}
	
}
