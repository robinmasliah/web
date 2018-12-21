/***
 * Class Job1Reducer
 * Job1 Reducer class
 * @author sgarouachi
 */

import java.io.IOException;
import java.util.SortedSet;
import java.util.TreeSet;

import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Job1Reducer extends Reducer<Text, Text, Text, Text> {

	/**
	 * Job1 Reduce method (page, 1.0 \t outLinks) Remove redundant links & sort
	 * them Asc
	 */
	@Override
	public void reduce(Text key, Iterable<Text> values, Context context)
			throws IOException, InterruptedException {
		// TODO if needed
		
		//Remove and sort redundant outLinks
        
        // Create a sorted set to store all the outlinks
        SortedSet<String> pages = new TreeSet<>();
    
        for (Text value: values ) {
            pages.add(value.toString());
        }
        
        String p = "";
        for (String page: pages ) {
            if (p != "")  p += ","  + page;
            else p = "" + page;
        }
        
        
        // Append default page rank + outLinks
        if("".equals(p)) {
        	context.write(key, new Text("1.0"));
        } else {
        	context.write(key, new Text("1.0\t"+p));
        }
		
	}
}
