use warnings;
use strict;
use v5.10;

open my $fin, '<', $ARGV[0];
local $/;
$_ = <$fin>;
close $fin;

my %simpleTranslate = ( 'b' => ['strong', ''], 'i' => ['em', ''], 's' => ['del', ''],
	'u' => ['span', ' style="text-decoration: underline;"'], 'ul' => ['ul', ''], 'li' => ['li', ''],
	'ol' => ['ol', ''], 'table' => ['table', ' style="border: 1px solid;"'], 'tr' => ['tr', ''],
	'td' => ['td', ''], 'quote(?:=\"[^\]]*\")?' => ['blockquote><p', ''],
	'code' => ['code', ' style="white-space: pre;"'] );

while (my ($BBTag, $HTMLTag) = each %simpleTranslate) {
	while(s/\[$BBTag\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<@{$HTMLTag}[0]@{$HTMLTag}[1]>".$1."<\/@{$HTMLTag}[0]>"/gse) {}
}

while(s/\[img\]((?:(?!\[img\]|\[\/img\]).)*)\[\/img\]/
	"<img src=\"$1\" \/>"/gse) {}

while(s/\[url\]((?:(?!\[url\]|\[\/url\]).)*)\[\/url\]/
		"<a href=\"$1\">".$1.'<\/a>'/gse) {}
while (s/\[url=([^\]]*)\]((?:(?!\[url\]|\[\/url\]).)*)\[\/url\]/
	"<a href=\"$1\">".$2.'<\/a>'/gse) {}

my %capturingTranslate = ( 'size' => 'font-size: ', 'color' => 'color: ' );

while (my ($BBTag, $CSSOption) = each %capturingTranslate) {
	while (s/\[$BBTag=\"([^\"]*)\"\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<span style=\"$CSSOption$1\;\">".$2.'<\/span>'/gse) {}
	while (s/\[$BBTag=([^\]]*)\]((?:(?!\[$BBTag\]|\[\/$BBTag\]).)*)\[\/$BBTag\]/
		"<span style=\"$CSSOption$1\;\">".$2.'<\/span>'/gse) {}
}

while (m/\[list\]((?:(?!\[list\]|\[\/list\]).)*)\[\/list\]/s) {
	my $list = $1 =~ s/\[\*\]/<li>/r;
	while ($list =~ s/\[\*\]/<\/li><li>/) {}
	$list =~ s/(?=\z)/<\/li>/;
	s/\[list\]((?:(?!\[list\]|\[\/list\]).)*)\[\/list\]/<ul>$list<\/ul>/s
}


while(m/\[style ([^\]]*)\]((?:(?!\[style\]|\[\/style\]).)*)\[\/style\]/) {
	my $style = $1 =~ s/\=/\:/gr;
	s/\[style ([^\]]*)\]((?:(?!\[style\]|\[\/style\]).)*)\[\/style\]/
	"<span style=\"$style\;\">".$2.'<\/span>'/gse
}

open my $fout, ">", "output.html";
say $fout $_;
close $fout;
