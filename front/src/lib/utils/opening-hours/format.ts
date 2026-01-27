import OpeningHours, { type optional_conf as OpeningConf } from "opening_hours";

const TIME_FORMATTER = new Intl.DateTimeFormat("fr-FR", {
  hour: "2-digit",
  minute: "2-digit",
  hour12: false,
});

const DAY_FORMATTER = new Intl.DateTimeFormat("fr-FR", {
  weekday: "short",
});

// 09:00-12:00,14:00-18:30 => 09h00 - 12:00 / 14h00 - 18h30
function formatHour(hour: string) {
  hour = hour.replace(/-/g, " - ");
  hour = hour.replace(/:/g, "h");
  hour = hour.replace(/,/g, " / ");
  return hour;
}

// Convertit l'index de jour JavaScript (0=dimanche) vers notre format (0=lundi)
function toDayIndex(jsDayIndex: number): number {
  return jsDayIndex === 0 ? 6 : jsDayIndex - 1;
}

// Formate les horaires d'un jour
function formatDayHours(dayIntervals: Array<[Date, Date]>): string {
  if (dayIntervals.length === 0) {
    return "Fermé";
  }

  // Trie les intervalles par heure de début
  const sortedIntervals = [...dayIntervals].sort(
    (a, b) => a[0].getTime() - b[0].getTime()
  );

  // Formate chaque intervalle en "HH:mm-HH:mm"
  const timeRanges = sortedIntervals.map(([start, end]) => {
    const startTime = TIME_FORMATTER.format(start);
    const endTime = TIME_FORMATTER.format(end);
    return `${startTime}-${endTime}`;
  });

  // Applique le formatage français (":" -> "h", "," -> " / ")
  return formatHour(timeRanges.join(","));
}

// Obtient le nom localisé d'un jour (ex: "Lun.")
function getDayName(dayIndex: number, weekStart: Date): string {
  const dayDate = new Date(weekStart);
  dayDate.setDate(weekStart.getDate() + dayIndex);
  const dayName = DAY_FORMATTER.format(dayDate);
  return dayName.charAt(0).toUpperCase() + dayName.slice(1);
}

export function formatOsmHours(value: string): Array<[string, string]> | null {
  try {
    const openingHoursInstance = new OpeningHours(value, null, {
      locale: "fr",
    } as OpeningConf);

    // Calcule le lundi de la semaine courante comme référence
    const now = new Date();
    const currentDay = now.getDay(); // 0 = dimanche, 1 = lundi, etc.
    const daysFromMonday = currentDay === 0 ? 6 : currentDay - 1;
    const weekStart = new Date(now);
    weekStart.setDate(now.getDate() - daysFromMonday);
    weekStart.setHours(0, 0, 0, 0);

    const weekEnd = new Date(weekStart);
    weekEnd.setDate(weekStart.getDate() + 7);

    // Récupère tous les intervalles ouverts de la semaine
    const intervals = openingHoursInstance.getOpenIntervals(weekStart, weekEnd);

    // Groupe les intervalles par jour de la semaine (0 = lundi, 6 = dimanche)
    const intervalsByDay: Array<Array<[Date, Date]>> = Array.from(
      { length: 7 },
      () => []
    );

    intervals.forEach(([start, end]) => {
      const dayIndex = toDayIndex(start.getDay());
      intervalsByDay[dayIndex].push([start, end]);
    });

    // Formate tous les jours de la semaine
    const formattedDays = intervalsByDay.map((dayIntervals, dayIndex) => {
      const hours = formatDayHours(dayIntervals);
      const isWeekday = dayIndex < 5; // 0-4 = lundi à vendredi

      // Toujours afficher les jours de semaine, même s'ils sont fermés
      if (isWeekday) {
        return [getDayName(dayIndex, weekStart), hours];
      }

      // Pour samedi-dimanche, n'afficher que s'ils ne sont pas fermés
      return hours !== "Fermé"
        ? [getDayName(dayIndex, weekStart), hours]
        : null;
    });

    // Filtre uniquement les jours weekend fermés (null) et retourne le résultat
    return formattedDays.filter((day): day is [string, string] => day !== null);
  } catch {
    // En cas d'erreur de parsing, retourne null pour indiquer un format invalide
    return null;
  }
}
