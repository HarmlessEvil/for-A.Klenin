use v5.10;
use strict;
use warnings;

use Data::Dumper;

use Cwd 'abs_path';
use DateTime;
use JSON;
use LWP::Simple;
use Time::Local;
use XML::Simple;

use Chart::Lines;

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

	my $i = 0;
	my @graphic = ( [], [] );

	foreach (@{$cubes[0]}) {
		if ($_->{time} lt $ARGV[2]) {
			do {
				foreach my $cube ($cubes[0][$i]->{Cube}[0]) {
					if ($cube->{currency} eq $ARGV[3]) {
						push @{$graphic[1]}, $cube->{rate};
						unshift @{$graphic[0]}, $cubes[0][$i]->{time};
						last;
					}
				}
			} while ($cubes[0][$i++]->{time} gt $ARGV[1]);
			last;
		}
		$i++;
	}

	my $chart = Chart::Lines->new(1000, 1000);
	$absCurrDir =~ s/\\(?!.*\\).*$/\\graphic.png/;

	$chart->set(
		'title'        => $ARGV[3],
		'x_label'      => "$ARGV[1]        $ARGV[2]",
		'y_label'      => "currency of $ARGV[3]",
		'skip_x_ticks' => 12
	);

	$chart->png($absCurrDir, \@graphic);

	exit;
} elsif ($ARGV[0] eq 'SBER') {
	my $currency = 'SBER.json';
	my $absCurrDir = abs_path($0);
	$absCurrDir =~ s/\\(?!.*\\).*$/\\SBER.txt/;

	my $val = $ARGV[3] eq 'USD' ? 3 : 2;

	my @temp = split '-', $ARGV[1];
	my $from;
	while (@temp) {
		$from .= '.' . pop @temp;
	}
	$from = substr($from, 1);

	@temp = split '-', $ARGV[2];
	my $to;
	while (@temp) {
		$to .= '.' . pop @temp;
	}
	$to = substr($to, 1);

	if (!-e "$currency") {
		getstore('http://www.sberbank.ru/common%2Fjs%2Fget_quote_values.php%3Fversion%3D1%26inf_block%3D123%26_number_amount114%3D10000%26qid%5B%5D=' . 
			$val . '%26cbrf%3D0%26period%3Don%26_date_afrom114%3D' . $from . 
			'%26_date_ato114%3D' . $to . '%26mode%3Dfull%26display%3Djson', $absCurrDir);
	}
	
	open(my $json, '<', $absCurrDir);
	say my $encoded = <$json>;

}

die 'Invalid input!';