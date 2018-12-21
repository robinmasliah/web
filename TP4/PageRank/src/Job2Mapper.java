/***
 * Class Job2Mapper
 * Job2 Mapper class
 * @author sgarouachi
 */

import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.SortedSet;
import java.util.TreeSet;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Mapper;

public class Job2Mapper extends Mapper<LongWritable, Text, Text, Text> {

	/**
	 * Job2 Map method Generates 3 outputs: Mark existing page: (pageI, !) Used
	 * to calculate the new rank (rank pageI depends on the rank of the inLink):
	 * (pageI, inLink \t rank \t totalLink) Original links of the page for the
	 * reduce output: (pageI, |pageJ,pageK...)
	 */
	@Override
	public void map(LongWritable key, Text value, Context context)
			throws IOException, InterruptedException {

		// TODO if needed
		String split[] = StringUtils.split(value.toString(), "\t");

		String var1 = split[0];
		String var2 = split[1];

		context.write(new Text(var1), new Text("!"));

		if (split.length == 3) {
			List<String> links = Arrays
					.asList(StringUtils.split(split[2], ','));
			for (String link : links) {

				context.write(new Text(link), new Text(var1 + "\t" + var2
						+ "\t" + links.size()));
			}

			context.write(new Text(var1),
					new Text("|" + StringUtils.join(links, ',')));
		}

	}
}
