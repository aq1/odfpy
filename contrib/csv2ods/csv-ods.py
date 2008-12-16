#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2008 Agustin Henze -> agustinhenze at gmail.com
#
# This is free software.  You may redistribute it under the terms
# of the Apache license and the GNU General Public License Version
# 2 or at your option any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public
# License along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
# Contributor(s):
#

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties, TableColumnProperties
from odf.text import P
from odf.table import Table, TableColumn, TableRow, TableCell
from optparse import OptionParser
import sys,csv,re

PWENC = "utf-8"

def csvToOds( pathFileCSV, pathFileODS, tableName='table', delimiter=',', quoting=csv.QUOTE_MINIMAL, quotechar = '"',
							escapechar = None, skipinitialspace = False, lineterminator = '\r\n'):
	textdoc = OpenDocumentSpreadsheet()
	# Create a style for the table content. One we can modify
	# later in the word processor.
	tablecontents = Style(name="Table Contents", family="paragraph")
	tablecontents.addElement(ParagraphProperties(numberlines="false", linenumber="0"))
	tablecontents.addElement(TextProperties(fontweight="bold"))
	textdoc.styles.addElement(tablecontents)
	
	# Create automatic styles for the column widths.
	# We want two different widths, one in inches, the other one in metric.
	# ODF Standard section 15.9.1
	widthshort = Style(name="Wshort", family="table-column")
	widthshort.addElement(TableColumnProperties(columnwidth="1.7cm"))
	textdoc.automaticstyles.addElement(widthshort)
	
	widthwide = Style(name="Wwide", family="table-column")
	widthwide.addElement(TableColumnProperties(columnwidth="1.5in"))
	textdoc.automaticstyles.addElement(widthwide)
	
	# Start the table, and describe the columns
	table = Table( name=tableName )
	table.addElement(TableColumn(numbercolumnsrepeated=4,stylename=widthshort))
	table.addElement(TableColumn(numbercolumnsrepeated=3,stylename=widthwide))
	
	reader = csv.reader(open(pathFileCSV), delimiter=delimiter,
						quoting=quoting, quotechar=quotechar, escapechar=escapechar,
						skipinitialspace=skipinitialspace, lineterminator=lineterminator)
	fltExp = re.compile('[-+]?[0-9]+\.[0-9]+$')
	intExp = re.compile("^[1-9]\d*$")
	
	for row in reader:
		tr = TableRow()
		table.addElement(tr)
		for val in row:
			if fltExp.match(val) or intExp.match(val):
				tc = TableCell(valuetype="float", value=float(val))  #Rounded to two digits
			else:
				tc = TableCell(valuetype="string")
			tr.addElement(tc)
			p = P(stylename=tablecontents,text=unicode(val,PWENC))
			tc.addElement(p)

	textdoc.spreadsheet.addElement(table)
	textdoc.save( pathFileODS )
	
if __name__ == "__main__":
	usage = "%prog -i file.csv -o file.ods -d \"&\""
	parser = OptionParser(usage=usage, version="%prog 0.1")
	parser.add_option('-i','--input', action='store',
			dest='input', help='File input in csv')
	parser.add_option('-o','--output', action='store',
			dest='output', help='File output in ods')
	parser.add_option('-d','--delimiter', action='store',
			dest='delimiter', help='specifies a one-character string to use as the field separator.  It defaults to ",".')
			
	parser.add_option('-c','--encoding', action='store',
			dest='encoding', help='specifies the encoding the file csv. It defaults utf-8')
			
	parser.add_option('-t','--table', action='store',
			dest='tableName', help='The table name in the output file')
			
	parser.add_option('-s','--skipinitialspace',
			dest='skipinitialspace', help='''specifies how to interpret whitespace which
						immediately follows a delimiter.  It defaults to False, which 
						means that whitespace immediately following a delimiter is part
						of the following field.''')
						
	parser.add_option('-l','--lineterminator', action='store',
			dest='lineterminator', help='''specifies the character sequence which should
						terminate rows.''')
						
	parser.add_option('-q','--quoting', action='store',
			dest='quoting', help='''It can take on any of the following module constants:
						0 = QUOTE_MINIMAL means only when required, for example, when a field contains either the quotechar or the delimiter
						1 = QUOTE_ALL means that quotes are always placed around fields.
						2 = QUOTE_NONNUMERIC means that quotes are always placed around fields which do not parse as integers or floating point numbers.
						3 = QUOTE_NONE means that quotes are never placed around fields.
						It defaults is QUOTE_MINIMAL''')
						
	parser.add_option('-e','--escapechar', action='store',
			dest='escapechar', help='''specifies a one-character string used to escape the delimiter when quoting is set to QUOTE_NONE.''')
			
	parser.add_option('-r','--quotechar', action='store',
			dest='quotechar', help='''specifies a one-character string to use as the quoting character.  It defaults to ".''')
						
	(options, args) = parser.parse_args()
	
	if options.input:
		pathFileCSV = options.input
	else:
		parser.print_help()
		exit( 0 )
		
	if options.output:
		pathFileODS = options.output
	else:
		parser.print_help()
		exit( 0 )
		
	if options.delimiter:
		delimiter = options.delimiter
	else:
		delimiter = ","
		
	if options.skipinitialspace:
		skipinitialspace = True
	else:
		skipinitialspace=False
	
	if options.lineterminator:
		lineterminator = options.lineterminator
	else:
		lineterminator ="\r\n"
	
	if options.escapechar:
		escapechar = options.escapechar
	else:
		escapechar=None
		
	if options.encoding:
		PWENC = options.encoding
		
	if options.tableName:
		tableName = options.tableName
	else:
		tableName = "table"
		
	if options.quotechar:
		quotechar = options.quotechar
	else:
		quotechar = "\""
		
	csvToOds( pathFileCSV=pathFileCSV, pathFileODS=pathFileODS, delimiter=delimiter, skipinitialspace=skipinitialspace,
						escapechar=escapechar, lineterminator=lineterminator, tableName=tableName, quotechar=quotechar)