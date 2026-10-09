# Contexto del proyecto - Trabajo Profesional FIUBA

Documento de referencia para agentes. Describe el alcance, la estructura y las convenciones de esta memoria LaTeX sin necesidad de releer todo el repositorio.

---

## 1. Identificaci�n acad�mica

| Campo | Valor |
|-------|-------|
| **Tipo de trabajo** | Trabajo Profesional |
| **Carrera** | Ingenier�a Electr�nica - FIUBA |
| **T�tulo** | Integraci�n de T�cnicas de Visi�n Computacional y Aprendizaje Autom�tico en un Robot Militar para la Identificaci�n y Eliminaci�n Eficiente de Objetivos |
| **Autores** | Lucas Mart�n Gaggino, Tom�s Jes�s Contessi |
| **Tutor** | Federico G. Zacchigna |
| **Lugar y fecha** | Ciudad de Buenos Aires, Agosto de 2025 (`portada.tex`) |
| **Palabras clave** | Sistemas Embebidos, Internet de las Cosas, Inteligencia Artificial |

---

## 2. Prop�sito del proyecto

Desarrollo de un **sistema rob�tico militar aut�nomo** capaz de identificar y neutralizar objetivos a�reos mediante visi�n computacional e IA. El trabajo integra:

1. **Simulador virtual** (Unreal Engine 5) para entrenar y validar algoritmos de forma segura y econ�mica.
2. **Prototipo f�sico (POC)** para validar movilidad, torreta, trackeo y disparo en condiciones controladas.
3. **Arquitectura de software modular** (POO, FSM, drivers abstractos sim/real) que conecta ambos entornos.

Objetivo f�sico concreto (objetivos particulares): detectar y neutralizar blancos de ~45x45 cm a 20 m de distancia.

---

## 3. Mapa del repositorio

```
trabajo_prof_memorias/
|-- memorianueva.tex          # Archivo maestro - compilar este
|-- portada.tex               # Portada con fondo Figures/fondo.pdf
|-- MastersDoctoralThesis.cls # Clase FIUBA/CESE - NO modificar
|-- references.bib            # Bibliografia BibTeX
|-- Chapters/
|   |-- presentacion.tex          # Wrapper -> input de subsecciones
|   |-- presentacion/
|   |   `-- alcance_y_objetivos.tex
|   |-- alcance_y_objetivos/      # Subsecciones reutilizadas desde presentacion
|   |-- introduccion_teorica.tex
|   |-- introduccion_teorica/
|   |-- analisis_tecnico.tex
|   |-- analisis_tecnico/
|   |-- analisis_mercado.tex
|   |-- analisis_mercado/
|   |-- prototipo.tex
|   |-- prototipo/
|   |-- simulador.tex
|   |-- simulador/
|   |-- pruebas_y_resultados.tex
|   |-- pruebas_y_resultados/
|   |-- conclusiones.tex
|   |-- conclusiones/
|   |-- Chapter1.tex ... Chapter5.tex   # Legacy/plantilla FIUBA - NO activos
|   `-- ChapterTemplate.tex             # Plantilla de ejemplo
|-- Appendices/
|   `-- AppendixA.tex
|-- Figures/                  # Imagenes finales (.png, .pdf, .jpg)
`-- scripts/
    |-- _common.py            # Utilidades compartidas
    |-- generate_prueba_*.py  # Generadores de figuras/metricas
    |-- run_all_prueba_assets.py
    |-- logs/*.json           # Metricas de pruebas virtuales
    `-- requirements-pruebas.txt
```

### Jerarqu�a LaTeX

- `memorianueva.tex` usa `\include{Chapters/<cap�tulo>}` para cap�tulos de primer nivel.
- Cada wrapper (`Chapters/<cap�tulo>.tex`) declara `\chapter{...}` y `\input{Chapters/<cap�tulo>/<secci�n>.tex}` para subsecciones.
- **Regla:** agregar secciones nuevas con `\input` en el wrapper del cap�tulo; solo tocar `memorianueva.tex` al a�adir un cap�tulo completamente nuevo.

---

## 4. Cap�tulos activos

| Orden | Archivo wrapper | Contenido |
|-------|-----------------|-----------|
| 1 | `Chapters/presentacion.tex` | Introducci�n, antecedentes, estado del arte, �reas profesionales, alcance y objetivos |
| 2 | `Chapters/introduccion_teorica.tex` | Fundamentos te�ricos (CV, IA, navegaci�n, control) |
| 3 | `Chapters/analisis_tecnico.tex` | An�lisis t�cnico del dise�o |
| 4 | `Chapters/analisis_mercado.tex` | Cliente objetivo, mercados, costos del prototipo |
| 5 | `Chapters/prototipo.tex` | Componentes, chasis, software, interfaz, conducci�n |
| 6 | `Chapters/simulador.tex` | Entorno UE5, validaci�n din�mica |
| 7 | `Chapters/pruebas_y_resultados.tex` | Pruebas virtuales y sobre prototipo f�sico |
| 8 | `Chapters/conclusiones.tex` | Conclusiones generales y pr�ximos pasos |

Ap�ndice: `Appendices/AppendixA.tex`

---

## 5. Dominio t�cnico

### Software (m�dulos principales)

Documentados en `Chapters/prototipo/software.tex`:

| M�dulo | Funci�n |
|--------|---------|
| **Control de misi�n** | FSM, coordinaci�n de subsistemas, transiciones por eventos |
| **Navegaci�n aut�noma** | Mapas de ocupaci�n, planificaci�n de trayectorias (A*) |
| **Seguimiento de objetivos** | Visi�n computacional, PID de torreta, condiciones de disparo |
| **Drivers abstractos** | Misma l�gica para simulador (gamepad virtual) y hardware real |
| **Colas de mensajes** | Comunicaci�n desacoplada entre procesos |

### M�quina de estados (FSM)

Estados principales: `STARTING`, `SENTINEL`, `TRACKING`, `TRACK_N_KILL`, `NAVIGATING`. Secundarios: `IDLE`, `PATROLLING`, `MAPPING`, `DEBUG`, `ERROR`. Diagrama en `Figures/maquina_de_estados.png`.

### Pruebas en simulaci�n (UE5)

| Archivo | Prueba |
|---------|--------|
| `prueba_slam_virtual.tex` | SLAM con LiDAR simulado |
| `prueba_path_planning_virtual.tex` | Planificaci�n de trayectorias A* |
| `prueba_localizacion_virtual.tex` | Localizaci�n global bajo ruido GPS |
| `prueba_fsm_evento_dinamico_virtual.tex` | FSM ante eventos din�micos |

Orquestadas desde `Chapters/pruebas_y_resultados/resultados_virtual.tex`.

### Pruebas sobre prototipo f�sico

| Archivo | Prueba |
|---------|--------|
| `prueba_movilidad_prototipo.tex` | Movilidad y superaci�n de terreno |
| `prueba_canon_prototipo.tex` | Desempe�o cinem�tico de torreta/ca��n |
| `prueba_trackeo_prototipo.tex` | Seguimiento de objetivos |
| `prueba_disparo_prototipo.tex` | Efectividad de neutralizaci�n |
| `prueba_trackeo_multiple_disparo.tex` | Trackeo m�ltiple y disparo |

### Scripts Python

- **Entrada:** datos externos en `D:\FIUBA\PROTECTOR\tactical_module\` (mapas, CSV de trayectorias) - definidos en `scripts/_common.py`.
- **Salida:** figuras en `Figures/` (ej. `prueba_localizacion_trayectorias.png`) y m�tricas JSON en `scripts/logs/`.
- **Ejecuci�n:** `python scripts/run_all_prueba_assets.py` regenera assets de pruebas 1-3 (SLAM, path planning, localizaci�n).

---

## 6. Plantilla de documentaci�n de pruebas

Toda prueba en `Chapters/pruebas_y_resultados/` sigue esta estructura de cuatro subsecciones:

```latex
\subsection{T�tulo de la prueba}

\subsubsection{Descripci�n de la prueba}
\paragraph{Objetivos m�nimos}
\begin{itemize} ... \end{itemize}

\subsubsection{Criterios de aprobaci�n}
\begin{table}[H]
  % columnas: M�trica | Criterio de aprobaci�n
  \label{tab:criterios_prueba_<nombre>}
\end{table}

\subsubsection{Procedimiento de ejecuci�n}
\begin{enumerate} ... \end{enumerate}

\subsubsection{Resultados}
\begin{table}[H]
  % columnas: M�trica | Resultado | Cumple (S�/No)
  \label{tab:resultados_prueba_<nombre>}
\end{table}
% Narrativa interpretando resultados + Figura~\ref{fig:...}
```

Tablas con `\toprule`, `\midrule`, `\bottomrule`. Float `[H]` (requiere paquete `float` en el pre�mbulo).

---

## 7. Convenciones LaTeX y de redacci�n

Basadas en la plantilla FIUBA (`Chapters/Chapter1.tex`, `Chapters/Chapter2.tex`) y el estilo adoptado en este documento.

### Redacci�n acad�mica FIUBA

| Contexto | Tiempo / estilo | Ejemplo |
|----------|-----------------|---------|
| Contenido de la memoria | Presente, impersonal | "En este cap�tulo se presentan las pruebas..." |
| Acciones del proyecto | Pasado, impersonal | "Se dise�� el firmware empleando..." |
| Referencias a partes | min�scula + `\ref` | "En el cap�tulo \ref{Chapter:Prototipo}..." |

- Evitar negritas (`\textbf`) en p�rrafos corridos; en listas de objetivos/pruebas s� se usa `\textbf{T�tulo:}` como convenci�n local.
- It�licas para extranjerismos: `\textit{digital filter}`.
- Comillas para citas textuales o t�rminos inventados.
- Abreviaturas explicadas en el cuerpo del texto, no en glosario separado.

### Referencias cruzadas

- Figuras: `Figura~\ref{fig:nombre}` - nunca "como se ve en la siguiente figura" sin `\ref`.
- Tablas: `Tabla~\ref{tab:nombre}`.
- `\label` despu�s de `\caption` en figuras.

### Matem�tica y unidades

```latex
$120\ \text{m}$           % distancia
$3{,}5\ \text{m}$         % coma decimal espa�ola
$180^\circ$               % grados
$\geq 2{,}0\ \text{m/s}$  % umbrales en tablas
```

### Figuras

```latex
\begin{figure}[H]  % o [htbp] seg�n contexto
\centering
\includegraphics[width=.9\textwidth]{Figures/nombre.png}
\caption{Descripci�n en espa�ol.}
\label{fig:nombre_snake_case}
\end{figure}
```

Rutas relativas desde la ra�z: `Figures/...`. Preferir PNG/PDF vectorial.

### Labels

Convenci�n mixta existente en el repo:

- Cap�tulos: `\label{Chapter:Nombre}` o `\label{Conclusiones}`
- Figuras: `\label{fig:snake_case}`
- Tablas de prueba: `\label{tab:criterios_prueba_*}` / `\label{tab:resultados_prueba_*}`
- Secciones legacy con espacios: `\label{Objetivos generales}`

**Al agregar contenido nuevo:** preferir `fig:` y `tab:` en snake_case sin espacios.

### Identificadores de c�digo / FSM

Usar `\texttt{TRACKING}`, `\texttt{SENTINEL}`, etc. para estados y nombres de m�dulo.

### Citas bibliogr�ficas

- Formato IEEE v�a biblatex/natbib: `\citep{clave}`.
- Entradas en `references.bib`.
- Compilaci�n: PDFLaTeX, luego BibTeX, luego PDFLaTeX dos veces.

### Cap�tulos

Cada cap�tulo debe comenzar con un p�rrafo introductorio que indique su contenido.

---

## 8. Compilaci�n

```bash
# Desde la ra�z del repo
pdflatex memorianueva.tex
bibtex memorianueva
pdflatex memorianueva.tex
pdflatex memorianueva.tex
```

**Dependencias TeXLive:** `texlive-lang-spanish`, `texlive-latex-extra`, `texlive-bibtex-extra`, `texlive-science`, paquetes `float`, `graphicx`, `hyperref`, `amsmath`, `eso-pic`.

**No versionar:** `*.aux`, `*.log`, `*.toc`, `*.lof`, `*.lot`, `*.out`, `*.bbl`, `*.blg`, `*.run.xml`, PDFs generados.

---

## 9. Fuera de scope para agentes

- **No inventar** resultados de pruebas, m�tricas ni veredictos de cumplimiento.
- **No modificar** `MastersDoctoralThesis.cls` salvo necesidad extrema y acordada.
- **No commitear** artefactos de compilaci�n ni PDFs de salida.
- **No asumir** hardware no documentado (ej. m�dulo GNSS NEO-6M a�n no integrado - ver `prueba_localizacion_virtual.tex`).
- **No expandir** el marco militar m�s all� del alcance acad�mico del TP.
- **No editar** cap�tulos legacy (`Chapter1.tex` a `Chapter5.tex`) salvo consulta de convenciones FIUBA.

---

## 10. Estado conocido del documento

| Elemento | Estado |
|----------|--------|
| Prueba localizaci�n virtual | **No cumple** criterios (error medio 19,68 m vs umbral 3,5 m) - valores en `prueba_localizacion_virtual.tex` y `scripts/logs/prueba_localizacion_metrics.json` |
| Telemetr�a del prototipo | Secci�n comentada en `prototipo.tex` (`%\input{.../telemetria}`) |
| Cap�tulos Chapter1-5 | Incluidos en repo como gu�a FIUBA; **no** compilados en `memorianueva.tex` |
| `references.bib` | Contiene entradas de ejemplo y reales mezcladas; verificar claves al citar |
| Rutas en `_common.py` | Apuntan a `D:\FIUBA\PROTECTOR\...` - entorno local del autor |

---

## 11. �reas profesionales de relevancia

Ingenier�a Electr�nica, Visi�n Computacional, IA/ML, Ingenier�a Mec�nica, Telecomunicaciones, Sistemas Embebidos, Fabricaci�n y Prototipado (`Chapters/presentacion/areas.tex`).
