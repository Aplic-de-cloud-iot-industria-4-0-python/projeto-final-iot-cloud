\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{ufersa}[2024/02/06 - Estácio]

% Packages

\LoadClass[a4, 12pt]{article}
\RequirePackage[brazilian]{babel}
\RequirePackage[utf8]{inputenc}
\RequirePackage{helvet}
\RequirePackage{indentfirst}
\RequirePackage{etoolbox}
\RequirePackage{geometry}
\RequirePackage{setspace}
\RequirePackage{titlesec}
\RequirePackage{tocloft}
\RequirePackage{graphicx}
\RequirePackage{fancyhdr}

% Personal data

\input{seus-dados}

% Document structure

\doublespacing
\renewcommand{\familydefault}{\sfdefault}
\pagestyle{fancy}
\geometry{margin=1in, bottom=2.5in}
\AtBeginDocument {\capa\conteudo}
\AtEndDocument {\assinaturas}

% Sections

\titleformat{\section}
  {\normalfont\bfseries}{\thesection.}{1em}{}[{\titlerule[0.8pt]}]
\titleformat{\subsection}
  {\normalfont\bfseries}{\thesubsection}{1em}{}

% Header and footer

\setlength\headheight{108pt}
\renewcommand{\headrulewidth}{0pt}

\lhead{}
\chead{%
  \includegraphics[width=3.5cm]{assets/logo}\\%
  \textbf{\footnotesize Universidade Estácio de Florianópolis}\\%
  % \footnotesize Departamento de Computação (DC)\\%
  Relatório sobre IoT%
}
\rhead{}

\lfoot{}
\rfoot{\thepage}
\cfoot{\data}

\fancypagestyle{coverstyle}
{
  \lfoot{}
  \rfoot{}
  \cfoot{}
}

% Summary

\addto\captionsbrazilian{%
  \renewcommand{\contentsname}%
    {\normalfont\bfseries Conteúdo}%
}

\newcommand{\agradecimentos}{%
  \section*{Agradecimentos}%
  Gostaríamos de expressar nossos sinceros agradecimentos a todas as pessoas que contribuíram para o desenvolvimento deste relatório. Em particular, agradecemos ao nosso professor pelo apoio e orientação ao longo do processo. Também agradecemos aos colegas de equipe pelo trabalho árduo e colaboração, que foram fundamentais para o sucesso deste projeto.
  \newpage % Nova página para o sumário
}

\newcommand{\conteudo}{\tableofcontents\thispagestyle{coverstyle}\newpage}

\renewcommand{\cftsecfont}{}
\renewcommand{\cftdotsep}{0.5}
\renewcommand{\cftsecleader}{\cftdotfill{\cftdotsep}}

% Signatures

\newcommand{\assinaturas}{\newpage\section{Assinaturas}%
\vspace{2cm}%
\begin{center}%
\vspace{2cm}%
\line(1,0){250}\\%
\emph{Assinatura do Aluno}\\%
\emph{\aluno}%
\end{center}%
\begin{center}%
\vspace{2cm}%
\vspace{2cm}%
\line(1,0){250}\\%
\emph{Assinatura do professor}\\%
\emph{\supervisorNome\enskip(\supervisorCargo)}%
\end{center}%
\begin{center}%
\vspace{2cm}%
\end{center}}

% Cover page

\newcommand{\capa}{\vspace*{10cm}%
\begin{flushright}%
\footnotesize%
\textbf{Aluno:} \aluno\\%
% \textbf{Supervisor na Estácio – Florianópolis:} \professorNome\\%
\textbf{Professor:} \supervisorNome\\%
\textbf{Faculdade:} \empresa\\%
% \textbf{Período de estágio:} \periodo\\%
\end{flushright}%
\vspace{1cm}%
\begin{center}%
\footnotesize%
\ifdef{\relatorioFinal}
  {\textbf{RELATÓRIO FINAL  [\quad] \hspace{1cm} RELATÓRIO PARCIAL [ X ]}\\}%
  {\textbf{RELATÓRIO FINAL [\quad] \hspace{1cm} RELATÓRIO PARCIAL [ X ]}\\}%
\vspace{1cm}%
\footnotesize%
\textbf{APROVADO [\quad] \hspace{1.5cm} REPROVADO [\quad] \hspace{1.5cm} AJUSTES [\quad]}%
\end{center}%
\thispagestyle{coverstyle}%
\newpage}
