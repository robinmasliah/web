/***
 * Class Job2Reducer
 * Job2 Reducer class
 * @author sgarouachi
 */

import java.io.IOException;

import org.apache.commons.lang.StringUtils;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Reducer;

public class Job2Reducer extends Reducer<Text, Text, Text, Text> {
	// Init dumping factor to 0.85
	private static final float damping = 0.85F;

	/**
	 * Job2 Reduce method Calculate the new page rank
	 */
	@Override
	public void reduce(Text page, Iterable<Text> values, Context context)
			throws IOException, InterruptedException {
		// For each otherPage:
		// - check control characters
		// - calculate pageRank share <rank> / count(<links>)
		// - add the share to sumShareOtherPageRanks

		// Write to output
		// (page, rank \t outLinks)
		// context.write(page, new Text(String.format(java.util.Locale.US,
		// "%.4f", newRank) + links));
		// TODO if needed
		boolean bpage = false;
		boolean blinks = false;
		String links = "";
		float sum = 0.0F;

		for (Text value : values) {
			if (value.toString().startsWith("!")) {
				bpage = Boolean.TRUE;
			} else {
				if (value.toString().startsWith("|")) {

					blinks = true;
					links = "\t" + value.toString().substring(1);
				} else {
					String[] split = StringUtils.split(value.toString(), '\t');
					sum = sum + Float.parseFloat(split[1])
							/ Integer.parseInt(split[2]);
				}
			}
		}

		if (bpage) {
			float newRank = 1.0F - damping + damping * sum;
			if (blinks) {
				context.write(
						page,
						new Text(String.format(java.util.Locale.US, "%.4f",
								newRank) + links));
			} else {
				context.write(
						page,
						new Text(String.format(java.util.Locale.US, "%.4f",
								newRank)));
			}
		}
	}
}
