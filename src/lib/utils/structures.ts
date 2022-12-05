export function formatOsmHours(value: string) {
  let monday = "Fermé";
  let tuesday = "Fermé";
  let wednesday = "Fermé";
  let thursday = "Fermé";
  let friday = "Fermé";
  let saturday = undefined;
  let sunday = undefined;

  const hoursByDay = value.split(";");

  hoursByDay.forEach((hoursForDay) => {
    const [dayPrefix, hours] = hoursForDay.split(" ");

    if (dayPrefix === "Mo") monday = formatHour(hours);
    if (dayPrefix === "Tu") tuesday = formatHour(hours);
    if (dayPrefix === "We") wednesday = formatHour(hours);
    if (dayPrefix === "Th") thursday = formatHour(hours);
    if (dayPrefix === "Fr") friday = formatHour(hours);
    if (dayPrefix === "Sa") saturday = formatHour(hours);
    if (dayPrefix === "Su") sunday = formatHour(hours);
  });

  return [
    ["Lun.", monday],
    ["Mar.", tuesday],
    ["Mer.", wednesday],
    ["Jeu.", thursday],
    ["Ven.", friday],
    saturday && ["Sam.", saturday],
    sunday && ["Dim.", sunday],
  ].filter(Boolean);
}

// 09:00-12:00,14:00-18:30 => 09h00 - 12:00 / 14h00 - 18h30
function formatHour(hour: string) {
  hour = hour.replace(/-/g, " - ");
  hour = hour.replace(/:/g, "h");
  hour = hour.replace(/,/g, " / ");
  return hour;
}
