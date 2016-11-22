
# for-A.Klenin
For homework and other projects

Project list:
- Converter BBCode to HTML
- Dates

use v5.10;
use strict;
use warnings;

use Data::Dumper;

use Cwd 'abs_path';
use DateTime;
use LWP::Simple;
use Time::Local;
use XML::Simple;

if (!@ARGV) {
	die 'Please, choose bank as argument of command line! Available banks: ECB - European Central Bank';
} elsif (@ARGV <= 2) {
	die 'please, add correct data range in format: "yyyy-mm-dd yyyy-mm-dd"';
} elsif (@ARGV < 4) {
	die 'Please, add currency';
}

if ($ARGV[0] eq 'ECB') {
	my $currency = 'ECB.xml';
	my $absCurrDir = abs_path($0);
	$absCurrDir =~ s/\\(?!.*\\).*$/\\ECB.xml/;

	if (!-e "$currency") {
		getstore('http://www.ecb.europa.eu/stats/eurofxref/eurofxref-hist.xml', $absCurrDir);
	}

	my $ref = XMLin($absCurrDir);
	my @cubes = sort {$a <=> $b} $ref->{Cube}{Cube};

	my ($i, @graphic) = 0;

	foreach (@{$cubes[0]}) {
		if ($_->{time} lt $ARGV[2]) {
			do {
				foreach my $cube ($cubes[0][$i]->{Cube}[0]) {
					if ($cube->{currency} eq $ARGV[3]) {
						push @graphic, $cube->{rate};
						last;
					}
				}
			} while ($cubes[0][$i++]->{time} gt $ARGV[1]);
			last;
		}
		$i++;
	}

	exit;
}

die 'Invalid input!';
