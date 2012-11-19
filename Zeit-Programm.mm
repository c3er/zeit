<map version="freeplane 1.2.0">
<!--To view this file, download free mind mapping software Freeplane from http://freeplane.sourceforge.net -->
<node TEXT="Zeit-Programm" FOLDED="false" ID="ID_140218298" CREATED="1317579750742" MODIFIED="1317579767278"><hook NAME="MapStyle">
    <properties show_note_icons="true"/>

<map_styles>
<stylenode LOCALIZED_TEXT="styles.root_node">
<stylenode LOCALIZED_TEXT="styles.predefined" POSITION="right">
<stylenode LOCALIZED_TEXT="default" MAX_WIDTH="600" COLOR="#000000" STYLE="as_parent">
<font NAME="SansSerif" SIZE="10" BOLD="false" ITALIC="false"/>
</stylenode>
<stylenode LOCALIZED_TEXT="defaultstyle.details"/>
<stylenode LOCALIZED_TEXT="defaultstyle.note"/>
<stylenode LOCALIZED_TEXT="defaultstyle.floating">
<edge STYLE="hide_edge"/>
<cloud COLOR="#f0f0f0" SHAPE="ROUND_RECT"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.user-defined" POSITION="right">
<stylenode LOCALIZED_TEXT="styles.topic" COLOR="#18898b" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subtopic" COLOR="#cc3300" STYLE="fork">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.subsubtopic" COLOR="#669900">
<font NAME="Liberation Sans" SIZE="10" BOLD="true"/>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.important">
<icon BUILTIN="yes"/>
</stylenode>
</stylenode>
<stylenode LOCALIZED_TEXT="styles.AutomaticLayout" POSITION="right">
<stylenode LOCALIZED_TEXT="AutomaticLayout.level.root" COLOR="#000000">
<font SIZE="18"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,1" COLOR="#0033ff">
<font SIZE="16"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,2" COLOR="#00b439">
<font SIZE="14"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,3" COLOR="#990000">
<font SIZE="12"/>
</stylenode>
<stylenode LOCALIZED_TEXT="AutomaticLayout.level,4" COLOR="#111111">
<font SIZE="10"/>
</stylenode>
</stylenode>
</stylenode>
</map_styles>
</hook>
<node TEXT="Programm zum Messen/Erfassen der eingesetzten Zeit" POSITION="right" ID="ID_894914387" CREATED="1343547122005" MODIFIED="1344181538270"/>
<node TEXT="Features / M&#xf6;glichkeiten" POSITION="right" ID="ID_942218652" CREATED="1344181019211" MODIFIED="1344181136564">
<node TEXT="Es soll Arbeitszeit erfasst werden" ID="ID_1848746208" CREATED="1344181064605" MODIFIED="1344181258858"/>
<node TEXT="Zeiterfassung f&#xfc;r *verschiedene* Projekte" ID="ID_910327537" CREATED="1344181482130" MODIFIED="1344181517265"/>
<node TEXT="Zu Protokollieren" ID="ID_1894158683" CREATED="1344181262467" MODIFIED="1344181269525">
<node TEXT="Uhrzeiten / Dauer" ID="ID_1351450346" CREATED="1344181313711" MODIFIED="1344212563175">
<node TEXT="Gesamtes Projekt" ID="ID_391797947" CREATED="1344212514713" MODIFIED="1344212526290">
<node TEXT="Unterteilbar in Unterprojekten" ID="ID_507756253" CREATED="1344212527193" MODIFIED="1344212537854"/>
</node>
<node TEXT="F&#xfc;r die jeweiligen Tage" ID="ID_488635239" CREATED="1344212540841" MODIFIED="1344212556083"/>
<node TEXT="F&#xfc;r den jeweiligen Abschnitt" ID="ID_1029359586" CREATED="1344212575204" MODIFIED="1344212594674"/>
<node TEXT="Pausen" ID="ID_1381114288" CREATED="1344181328958" MODIFIED="1344181331737">
<node TEXT="Es k&#xf6;nnen beliebig viele Pausen zwischen den Abschnitten vorhanden sein" ID="ID_1305634726" CREATED="1344213430893" MODIFIED="1344213476787"/>
</node>
</node>
</node>
<node TEXT="Bedienung" ID="ID_299427308" CREATED="1344212897038" MODIFIED="1344212901017">
<node TEXT="Anzeige" ID="ID_104621226" CREATED="1344213551381" MODIFIED="1344213554863">
<node TEXT="Abschnitt f&#xfc;r die aktuell aufgenommene Zeit" ID="ID_166741582" CREATED="1344213635529" MODIFIED="1344214459956">
<node TEXT="Von oben nach unten" ID="ID_1801705817" CREATED="1344214591424" MODIFIED="1346017052084"><richcontent TYPE="NOTE">

<html>
  <head>
    
  </head>
  <body>
    <p>
      (Oder von Links nach rechts)
    </p>
  </body>
</html>
</richcontent>
<node TEXT="Abschnitt" ID="ID_977305979" CREATED="1344214605960" MODIFIED="1347229955813">
<node TEXT="hh:mm" ID="ID_219867079" CREATED="1344371188960" MODIFIED="1347230839948"/>
</node>
<node TEXT="Pause" ID="ID_1754837730" CREATED="1347229946606" MODIFIED="1347229950108">
<node TEXT="hh:mm" ID="ID_257143692" CREATED="1344371188960" MODIFIED="1347230839948"/>
<node TEXT="Wenn Pause ist, wird die Pausenzeit von Null hochgez&#xe4;hlt und&#xa;die anderen Zeiten werden angehalten" ID="ID_53246947" CREATED="1344214778644" MODIFIED="1347230820597"/>
</node>
<node TEXT="Tag" ID="ID_1728740554" CREATED="1344214628136" MODIFIED="1344214641667">
<node TEXT="hh:mm" ID="ID_610077942" CREATED="1344371231185" MODIFIED="1344371237473"/>
</node>
<node TEXT="Unterprojekt" ID="ID_1484714902" CREATED="1344214645259" MODIFIED="1344214669120">
<node TEXT="ww:dd:hh:mm" ID="ID_1372192732" CREATED="1344371240720" MODIFIED="1344398468395"/>
<node TEXT="Jeweils eine Anzeige f&#xfc;r jede Hierarchieebene bis zum Gesamtprojekt" ID="ID_933128480" CREATED="1344214669889" MODIFIED="1344214763367"/>
<node TEXT="Wenn es kein Unterprojekt gibt, gibt es auch keine Anzeige" ID="ID_367629930" CREATED="1346018099718" MODIFIED="1346018131216"/>
</node>
<node TEXT="Projekt" ID="ID_1392247566" CREATED="1344214765400" MODIFIED="1344214772342">
<node TEXT="ww:dd:hh:mm" ID="ID_1282613972" CREATED="1344371308734" MODIFIED="1344398474653"/>
</node>
</node>
<node TEXT="Im Debug-Modus werden zus&#xe4;tzlich die Sekunden angezeigt" ID="ID_236670886" CREATED="1344371730121" MODIFIED="1344371751950"/>
</node>
<node TEXT="Protokollansicht der aufgenommenen Zeiten" ID="ID_1815719865" CREATED="1344213707269" MODIFIED="1344213724632">
<node TEXT="Alle relevanten Zeiten f&#xfc;r das jeweilige Projekt" ID="ID_599724330" CREATED="1344213725497" MODIFIED="1344215449329">
<node TEXT="Start/Ende" ID="ID_1797851177" CREATED="1344215021242" MODIFIED="1344215025801">
<node TEXT="des Projektes" ID="ID_350976561" CREATED="1344214918544" MODIFIED="1344215413294">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_394371064" STARTINCLINATION="85;0;" ENDINCLINATION="85;0;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
</node>
<node TEXT="des jeweiligen Unterprojektes" ID="ID_1748348726" CREATED="1344214948799" MODIFIED="1344215405723">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_394371064" STARTINCLINATION="119;0;" ENDINCLINATION="119;0;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
</node>
<node TEXT="der jeweiligen Tage" ID="ID_1124620167" CREATED="1344214967692" MODIFIED="1344215393558">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_394371064" STARTINCLINATION="62;0;" ENDINCLINATION="62;0;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
</node>
<node TEXT="der jeweiligen Abschnitten/Pausen" ID="ID_46450898" CREATED="1344215056088" MODIFIED="1344215383395">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_394371064" STARTINCLINATION="129;0;" ENDINCLINATION="129;0;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
</node>
</node>
<node TEXT="Die Dauer von allen Teilen" ID="ID_394371064" CREATED="1344215250758" MODIFIED="1344215289316">
<node TEXT="Wird in dem jeweiligen Datensatz vom Ende angezeigt" ID="ID_1989572635" CREATED="1346018255904" MODIFIED="1346018290182"/>
</node>
</node>
<node TEXT="Spalten" ID="ID_111039168" CREATED="1346018612256" MODIFIED="1346018618632">
<node TEXT="Datum" ID="ID_787527928" CREATED="1346575870744" MODIFIED="1346575878103"/>
<node TEXT="Uhrzeit" ID="ID_256128419" CREATED="1346575879306" MODIFIED="1346575882339"/>
<node TEXT="..." ID="ID_1682927852" CREATED="1346576492154" MODIFIED="1346576494164"/>
</node>
</node>
</node>
<node TEXT="Button-Leiste" ID="ID_255096604" CREATED="1344213036435" MODIFIED="1346018448139">
<node TEXT="Zeit starten/pausieren" ID="ID_1848877464" CREATED="1344213049799" MODIFIED="1344213071633">
<node TEXT="Beim ersten Starten wird auch der Tag begonnen" ID="ID_1706234130" CREATED="1344213210293" MODIFIED="1344213232300"/>
</node>
<node TEXT="Tag beenden" ID="ID_1346427581" CREATED="1344213074722" MODIFIED="1344213098399">
<node TEXT="Bevor die Zeit zum ersten mal gestartet wurde, ist dieser Button grau" ID="ID_959808111" CREATED="1346018813208" MODIFIED="1346018855257"/>
</node>
</node>
<node TEXT="Men&#xfc;" ID="ID_1243366018" CREATED="1344213266894" MODIFIED="1346018466810">
<node TEXT="Projekt" ID="ID_732915188" CREATED="1344276956286" MODIFIED="1344276961188">
<node TEXT="Neues Projekt" ID="ID_131579162" CREATED="1344213285124" MODIFIED="1344213293660"/>
<node TEXT="Projekt &#xf6;ffnen" ID="ID_1590049415" CREATED="1344272678589" MODIFIED="1344272684418"/>
<node TEXT="Projekt speichern" ID="ID_215680502" CREATED="1346197621340" MODIFIED="1346197628624"/>
<node TEXT="Projekt speichern unter" ID="ID_1074832523" CREATED="1346197785233" MODIFIED="1346197796014"/>
<node TEXT="Projekt schlie&#xdf;en" ID="ID_386192765" CREATED="1344263971524" MODIFIED="1344276853479"/>
</node>
<node TEXT="Unterprojekt" ID="ID_590827364" CREATED="1344276961659" MODIFIED="1344276965493">
<node TEXT="Neues Unterprojekt" ID="ID_1163083311" CREATED="1344213295593" MODIFIED="1344213303061">
<node TEXT="Unterprojekte k&#xf6;nnen beliebig tief inneinander verschachtelt sein" ID="ID_1777017412" CREATED="1344213304164" MODIFIED="1344213344288"/>
</node>
<node TEXT="Unterprojekt fortsetzen" ID="ID_1410142747" CREATED="1344276888031" MODIFIED="1344276904144"/>
<node TEXT="Unterprojekt schlie&#xdf;en" ID="ID_1507382815" CREATED="1344263964340" MODIFIED="1344276884950"/>
</node>
<node TEXT="Tag" ID="ID_1086022171" CREATED="1346581979635" MODIFIED="1346581982773">
<node TEXT="Starten/Pausieren" ID="ID_424480930" CREATED="1346581985819" MODIFIED="1346581995442"/>
<node TEXT="Beenden" ID="ID_127159103" CREATED="1346581999897" MODIFIED="1346582018870"/>
<node TEXT="Zum Unterprojekt zuordnen..." ID="ID_1794875956" CREATED="1346582034256" MODIFIED="1346582053868"/>
</node>
</node>
<node TEXT="Sonstiges" ID="ID_954277103" CREATED="1344263980715" MODIFIED="1344263991000">
<node TEXT="Jedes Projekt wird in eine eigene Datei gespeichert" ID="ID_1931952674" CREATED="1344273009577" MODIFIED="1344273023946"/>
<node TEXT="Beim Programmstart wird das zuletzt ge&#xf6;ffnete Projekt automatisch wieder ge&#xf6;ffnet" ID="ID_1182355663" CREATED="1344366846239" MODIFIED="1344366887641"/>
<node TEXT="Wenn das Programm zum ersten mal gestartet wird oder das Projekt beim letzten mal geschlossen wurde, wird ein neues Projekt mit dem vorl&#xe4;ufigen Namen &quot;Unbenannt&quot; erstellt" ID="ID_1073066797" CREATED="1346578069194" MODIFIED="1346578210326">
<node TEXT="Das geschieht durch Laden einer &quot;Default&quot;-Datei" ID="ID_958692807" CREATED="1349008990735" MODIFIED="1349009057096">
<arrowlink SHAPE="CUBIC_CURVE" COLOR="#000000" WIDTH="2" TRANSPARENCY="80" FONT_SIZE="9" FONT_FAMILY="SansSerif" DESTINATION="ID_122709268" STARTINCLINATION="996;0;" ENDINCLINATION="996;0;" STARTARROW="NONE" ENDARROW="DEFAULT"/>
</node>
</node>
</node>
</node>
<node TEXT="Dateiformat" ID="ID_122709268" CREATED="1348006591920" MODIFIED="1352605056969">
<node TEXT="XML &#xe4;hnliches Format" ID="ID_695526528" CREATED="1348007097081" MODIFIED="1348007117251"/>
<node TEXT="Struktur" ID="ID_1809499488" CREATED="1352599049128" MODIFIED="1352599054932">
<node TEXT="&quot;projectfile&quot;" ID="ID_1699315358" CREATED="1352599107296" MODIFIED="1352599381152">
<node TEXT="Wurzelement" ID="ID_1769260655" CREATED="1352599356781" MODIFIED="1352599359247"/>
<node TEXT="Attribute" ID="ID_1546858198" CREATED="1352599134980" MODIFIED="1352599143948">
<node TEXT="&quot;version&quot;" ID="ID_1276948298" CREATED="1352599145084" MODIFIED="1352599389222">
<node TEXT="Enth&#xe4;lt die Versionsnummer der Datei" ID="ID_1213233436" CREATED="1352599338385" MODIFIED="1352599341440"/>
</node>
</node>
<node TEXT="&quot;starttime&quot;" ID="ID_643094141" CREATED="1352599253015" MODIFIED="1352599431538">
<node TEXT="Das Datum und die Uhrzeit, an der die Datei / das Projekt angelegt wurde" ID="ID_989293277" CREATED="1352599309173" MODIFIED="1352599440405"/>
</node>
</node>
</node>
</node>
</node>
<node TEXT="Sonstiges" POSITION="right" ID="ID_1677493891" CREATED="1344273267526" MODIFIED="1344273271879">
<node TEXT="Programm soll auch als Exe-Datei vorhanden sein" ID="ID_1164933354" CREATED="1344273273344" MODIFIED="1344273300815"/>
</node>
</node>
</map>
