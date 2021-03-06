/**
 * CellProfiler is distributed under the GNU General Public License.
 * See the accompanying file LICENSE for details.
 *
 * Copyright (c) 2003-2009 Massachusetts Institute of Technology
 * Copyright (c) 2009-2014 Broad Institute
 * All rights reserved.
 * 
 * Please see the AUTHORS file for credits.
 * 
 * Website: http://www.cellprofiler.org
 */
package org.cellprofiler.imageset.filter;

import org.cellprofiler.imageset.OMEMetadataExtractor;

/**
 * @author Lee Kamentsky
 * 
 * A predicate that determines whether an image plane
 * is a color image.
 *
 */
public class IsMonochromePredicate extends
		AbstractTerminalPredicate<ImagePlaneDetails> {
	final static public String SYMBOL="ismonochrome";

	protected IsMonochromePredicate() {
		super(ImagePlaneDetails.class);
	}

	/* (non-Javadoc)
	 * @see org.cellprofiler.imageset.filter.FilterPredicate#getSymbol()
	 */
	public String getSymbol() {
		return SYMBOL;
	}

	/* (non-Javadoc)
	 * @see org.cellprofiler.imageset.filter.FilterPredicate#eval(java.lang.Object)
	 */
	public boolean eval(ImagePlaneDetails candidate) {
		if (! candidate.metadata.containsKey(OMEMetadataExtractor.MD_COLOR_FORMAT)) return false;
		return candidate.metadata.get(OMEMetadataExtractor.MD_COLOR_FORMAT).equals(
				OMEMetadataExtractor.MD_MONOCHROME);
	}

}
