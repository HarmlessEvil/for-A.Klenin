package Dates; {

	use warnings;
	use v5.10;
	use strict;
	use overload ('+' => 'addDate', 'eq' => 'equal', '-' => 'dateDiff');

	my @months = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31);
	my @weekday = ("mon", "tue", "wen", "thu", "fri", "sat", "sun");

	sub new {
		my $class = shift;
		my @dataParts = split /\./, shift;

		die 'Wrong date format' if @dataParts != 3;
		die 'Format of year has to be YYYY' if length $dataParts[2] != 4;
		die 'Format of month has to be MM' if length $dataParts[1] != 2;
		die 'Format of day has to be DD' if length $dataParts[0] != 2;

		die 'Invalid year' if $dataParts[2] <= 0;
		die 'Invalid month' if (($dataParts[1] < 1) || ($dataParts[1] > 12));

		my $daysAmount = ($dataParts[2] - 1) * 365.2425;
		if ((($dataParts[2] % 4 == 0) && ($dataParts[2] % 100 != 0)) || ($dataParts[2] % 400 == 0)) {
			$months[1]++;
			die 'Invalid day' if (($dataParts[0] <= 0) || ($dataParts[0] > $months[$dataParts[1] - 1]));
		}

		for (0 .. $dataParts[1] - 2) {
			$daysAmount += $months[$_];
		}
		$daysAmount += $dataParts[0] - 1;

		my $self = {
			daysAmount => $daysAmount
		};

		if ((($dataParts[2] % 4 == 0) && ($dataParts[2] % 100 != 0)) || ($dataParts[2] % 400 == 0)) {
			$months[1]--;
		}

		bless $self, $class;

		return $self;
	}

	sub addDate {
		my $self = shift;
		my $otherDate = shift;
		my $result = Dates->new($self->printDate());
		
		$result->{daysAmount} = $otherDate->{daysAmount} + $self->{daysAmount};

		return $result;
	}

	sub equal {
		my $self = shift;
		my $otherDate = shift;

		return $self->{daysAmount} == $otherDate->{daysAmount};
	}

	sub dateDiff {
		my $self = shift;
		my $otherDate = shift;

		return abs(int($self->{daysAmount}) - int($otherDate->{daysAmount}));
	}

	sub addDay {
		my $self = shift;
		my $days = shift;
		my $koef = int($days / 365.2425);

		my $before = int($self->{daysAmount} / 365.2425);
		$self->{daysAmount} += $days + $koef;
		my $after = int($self->{daysAmount} / 365.2425);

		if (($after - $before) != $koef) {
			$self->{daysAmount} += (0.2425 - 1);
		}

		die 'Invalid date' if $self->{daysAmount} < 0;
	}

	sub isLeapYear {
		my $year = shift;

		return (($year % 4 == 0) && ($year % 100 != 0)) || ($year % 400 == 0);
	}

	sub getYear {
		my $self = shift;

		return int($self->{daysAmount} / 365.2425) + 1;
	}

	sub getMonth {
		my $self = shift;
		my $days = $self->{daysAmount};
		my $year = $self->getYear();

		$days -= ($year - 1) * 365.2425;
		$days = int($days);

		if (isLeapYear($year - 1)) {
			$months[1]++;
		}

		my $month = 0;
		while ($days >= $months[$month]) {
			$days -= $months[$month];
			$month++;
		}
		if ($days > 0) {
			$month++;
		}
		

		if (isLeapYear($year - 1)) {
			$months[1]--;
		}

		return $month;
	}

	sub getDay {
		my $self = shift;

		my $days = $self->{daysAmount};
		my $year = $self->getYear();
		$days -= ($year - 1) * 365.2425;

		$days = int($days);
		
		if (isLeapYear($year)) {
			$months[1]++;
		}

		my $month = $self->getMonth();
		for (0 .. $month - 2) {
			$days -= $months[$_];
		}
		$days = $days == $months[$month - 1] ? 0 : $days;

		if (isLeapYear($year)) {
			$months[1]--;
		}

		return ++$days;
	}

	sub getWeekDay {
		my $self = shift;

		return $weekday[int($self->{daysAmount}) % 7];
	}

	sub printDate {
		my $self = shift;

		my $year = $self->getYear();
		my $month = $self->getMonth();
		my $day = $self->getDay();

		$day = $day < 10 ? '0'.$day : $day;
		$month = $month < 10 ? '0'.$month : $month;
		$year = $year < 10 ? '000'.$year : $year < 100 ? '00'.$year : $year < 1000 ? '0'.$year : $year;

		return "$day.$month.$year";
	}

	sub setYear {
		my $self = shift;
		my $year = shift;

		die 'Invalid year' if $year <= 0;

		if ($self->getMonth() > 2) {

			if ((isLeapYear($self->getYear())) && (!isLeapYear($year))) {
				$self->{daysAmount}--;
			} elsif ((!isLeapYear($self->getYear())) && (isLeapYear($year))) {
				$self->{daysAmount}++;
			}
		}

		$self->{daysAmount} -= ($self->getYear() - 1) * 365.2425;
		$self->{daysAmount} = int($self->{daysAmount});
		$self->{daysAmount} += ($year - 1) * 365.2425;
	}

	sub setMonth {
		my $self = shift;
		my $month = shift;

		my $year = $self->getYear() - 1;
		my $day = $self->getDay() - 1;

		$self->{daysAmount} = $year * 365.2425;

		for (0 .. $month - 2) {
			$self->{daysAmount} += $months[$_];
		}

		$self->{daysAmount} += $day;
	}

	sub setDay {
		my $self = shift;
		my $day = shift;

		$self->{daysAmount} = $self->{daysAmount} - $self->getDay() + $day;
	}
}

1;