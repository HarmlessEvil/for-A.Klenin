use warnings;
use strict;
use v5.10;

open my $fin, '<', $ARGV[0];
local $/;
$_ = <$fin>;
close $fin;

my %simpleTranslate = ( 'b' => 'strong', 'i' => 'em', 's' => 'del' );

while (my ($BBTag, $HTMLTag) = each %simpleTranslate) {
	while (s/\[$BBTag\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<$HTMLTag>".$1."<\/$HTMLTag>"/ge) {}
}

my %translateParameter = ( 'u' => ['span style="text-decoration: line-through;"', 'span'],
						   'code' => ['code style="white-space: pre;"', 'code'] );

while (my ($BBTag, @HTMLTag) = each %translateParameter) {
	while (s/\[$BBTag\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<$HTMLTag[0][0]>".$1."<\/$HTMLTag[0][1]>"/ge) {}
}
=pod
my %translateParameterInside = (  );

while (s/\[$BBTag=(.*)\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<$HTMLTag[0][0]>".$2."<\/$HTMLTag[0][1]>"/ge) {}
=cut
open my $fout, '>', 'output.html';
say $fout $_;
close $fout;