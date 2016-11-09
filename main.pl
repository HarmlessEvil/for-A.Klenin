use warnings;
use strict;
use v5.10;
use Dates;
use Test::More tests => 17;

my $g = Dates->new('09.11.2016');
my $h = Dates->new('25.04.1307');
my $c = Dates->new('01.01.0999');
my $f = $g + $c;
is_deeply($g + $c, $f, 'addDate()');
ok($f->printDate() eq '10.11.3014', 'addDate()');
ok(($h - $c) eq '112608', 'dateDiff()');

my $d = Dates->new('31.12.2016');
$d->addDay(999999999999999);
ok($d->printDate() eq '01.06.2745403143784', 'addDay()');
$d->addDay(-1);
ok($d->printDate() =~ /^31\.05/, 'valid date after incrementing');

my $e = Dates->new('01.01.0001');
ok($e->getWeekDay() eq 'mon', 'getWeekDay()');
ok($g->getWeekDay() eq 'wen', 'getWeekDay() --- ~today is wendesday, hooray!');

ok($g->getYear() eq '2016', 'getYear()');
ok($h->getYear() eq '1307', 'getYear()');

ok($g->getMonth() eq '11', 'getMonth()');
ok($h->getMonth() eq '4', 'getMonth()');

ok($g->getDay() eq '9', 'getDay()');
ok($h->getDay() eq '25', 'getDay()');

$h->setYear(1996);
ok($h->getYear() eq '1996', 'setYear()');
ok($h->printDate() =~ /^25\.04/, 'didn\'t changes other numbers');

$h->setMonth(8);
ok($h->printDate() eq '24.08.1996', 'setMonth()');

$h->setDay(1);
ok($h->printDate() eq '01.08.1996', 'setDay()');